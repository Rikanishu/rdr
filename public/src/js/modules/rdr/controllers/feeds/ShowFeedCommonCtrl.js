angular.module('rdr')
    .controller("feeds.ShowFeedCommonCtrl", [
        '$injector', '$rootScope', '$scope', '$state', '$sce', '$timeout',
        'feedsService', 'articlesService', 'subscribesService', 'offlineReadQueueService',
        'hotkeys', 'scrollTo',  'options',
        function($injector, $rootScope, $scope, $state, $sce, $timeout,
                 feedsService, articlesService, subscribesService, offlineReadQueueService,
                 hotkeys, scrollTo, options) {

            if (!options.loadCallback) {
                throw new Error('Load callback is required');
            }

            var VIEW_TYPE_LIST = 'list';
            var VIEW_TYPE_PREVIEW = 'preview';

            var loadCurrentPage = 1;

            var readArticleLoadId = null;
            var readArticleCancelDef = null;
            var isReadArticleAllowed = true;

            $scope.isFavorites = options.isFavorites || false;
            $scope.cannotBeUpdated = options.cannotBeUpdated || false;
            $scope.cannotBeSubscribed = options.cannotBeSubscribed || false;
            $scope.cannotHaveUnread = options.cannotHaveUnread || false;
            $scope.viewType = VIEW_TYPE_LIST;
            $scope.pageLoading = true;
            $scope.searchFormModel = {
                query: ''
            };

            options.loadCallback(loadCurrentPage).then(function(result) {

                $scope.pageLoading = false;
                reloadArticles(result);

                $scope.onArticleExpand = function(article) {
                    expandArticle(article);
                };

                $scope.loadMore = function() {
                    if (!$scope.paginationEndReached && !$scope.pageLoad) {
                        $scope.pageLoad = true;
                        $scope.paginationEndReached = true;
                        ++loadCurrentPage;
                        options.loadCallback(loadCurrentPage).then(function(result) {
                            if (result.articles && result.articles.length) {
                                updateArticlesHtml(result.articles);
                                $scope.feed.articles = $scope.feed.articles.concat(result.articles);
                                $scope.paginationEndReached = false;
                            }
                        }).finally(function() {
                            $scope.pageLoad = false;
                        })
                    }
                };

                /**
                 * Read fill text
                 *
                 * @param article
                 * @param e
                 */
                $scope.onReadArticle = function(article, e) {
                    e.preventDefault();
                    if ($scope.viewType === VIEW_TYPE_PREVIEW) {
                        openFullTextArticle(article);
                    } else {
                        articlesService.openFullText(article);
                    }

                };

                /**
                 * Close full text window
                 *
                 * @param e
                 */
                $scope.onReadArticleClose = function(e) {
                    e.preventDefault();
                    closeFullTextArticle();
                    $scope.viewType = VIEW_TYPE_LIST;
                };

                $scope.onAddToFavorites = function(article, e) {
                    e.preventDefault();
                    if (!article.isInFavorites) {
                        article.favoritesCount++;
                        feedsService.addArticleToFavorites(article);
                    } else {
                        article.favoritesCount--;
                        feedsService.removeArticleFromFavorites(article);
                    }
                };

                $scope.markAllAsRead = function(e) {
                    e.preventDefault();
                    var promise;
                    if (options.markAllAsReadCallback) {
                        promise = options.markAllAsReadCallback($scope);
                    } else if ($scope.feed.id) {
                        promise = feedsService.markFeedArticlesAsRead($scope.feed.id);
                    }
                    if (promise) {
                        promise.then(function(res) {
                            if (res.success) {
                                angular.forEach($scope.feed.articles, function(article) {
                                    if (!article.isRead) {
                                        article.isRead = true;
                                        $scope.$emit('article:read', article, $scope.feed);
                                    }
                                });
                            }
                        });
                    }
                };

                $scope.setViewTypePreview = function(e) {
                    e.preventDefault();
                    setViewTypePreview();
                };

                $scope.setViewTypeList = function(e) {
                    e.preventDefault();
                    setViewTypeList();
                };

                $scope.syncArticles = function(e) {
                    e.preventDefault();
                    if ($scope.feed.id) {
                        $scope.articlesLoading = true;
                        feedsService.syncArticles($scope.feed.id).then(function(result) {
                            reloadArticles(result);
                            $scope.articlesLoading = false;
                        });
                    }
                };

                $scope.onSearchFormSubmit = function(e) {
                    e.preventDefault();
                    if ($scope.searchFormModel.query) {
                        if (options.searchCallback) {
                            options.searchCallback($state, $scope)
                        } else {
                            if ($scope.feed.id) {
                                $state.go('home.searchFeed', {
                                    'feed': $scope.feed.id,
                                    'term': $scope.searchFormModel.query,
                                    'type': 'all',
                                    'where': ['title', 'announce', 'text'].join(',')
                                });
                            }
                        }
                    }
                };

                $scope.subscribe = function(e) {
                    e.preventDefault();
                    if (!$scope.feed.isSubscribed) {
                        subscribesService.newSubscribe({
                            packageId: $scope.feed.id,
                            packageType: $scope.feed.type,
                            folder: 0
                        }).then(function() {
                            $scope.feed.isSubscribed = true;
                            $rootScope.$emit('subscribes:refresh', {
                                active: $scope.feed
                            });
                        });
                    }
                };

                $scope.addArticleToOfflineQueue = function(article, e) {
                    e.preventDefault();
                    offlineReadQueueService.addArticleToQueue(article.id);
                };

                $scope.addUnreadToOfflineQueue = function(e) {
                    e.preventDefault();
                    if ($scope.feed.id) {
                        offlineReadQueueService.addFeedUnreadToQueue($scope.feed.id);
                    }
                }

            });

            /* Key bindings */
            hotkeys.bindTo($scope)
                .add({
                    combo: 'up',
                    description: 'Previous publication',
                    callback: function() {
                        if (!articlesService.isFullTextOpened()) {
                            if ($scope.feed && $scope.feed.articles && $scope.feed.articles.length > 0) {
                                var selectedArticle = $scope.selectedArticle;
                                if (!selectedArticle) {
                                    expandArticle($scope.feed.articles[0]);
                                } else {
                                    var currentArticleIndex = $scope.feed.articles.indexOf(selectedArticle);
                                    if (currentArticleIndex !== -1) {
                                        var nextArticleIndex = currentArticleIndex - 1;
                                        if (nextArticleIndex < 0) {
                                            nextArticleIndex = 0;
                                        }
                                    }
                                    var nextArticle = $scope.feed.articles[nextArticleIndex];
                                    expandArticle(nextArticle, {
                                        switchCallback: function() {
                                            scrollTo.id('article-' + nextArticle.id);
                                        }
                                    });
                                }
                            }
                        }
                    }
                })
                .add({
                    combo: 'down',
                    description: 'Next publication',
                    action: 'keydown',
                    callback: function() {
                        if (!articlesService.isFullTextOpened()) {
                            if ($scope.feed && $scope.feed.articles && $scope.feed.articles.length > 0) {
                                var selectedArticle = $scope.selectedArticle;
                                if (!selectedArticle) {
                                    expandArticle($scope.feed.articles[0]);
                                } else {
                                    var currentArticleIndex = $scope.feed.articles.indexOf(selectedArticle);
                                    if (currentArticleIndex !== -1) {
                                        var nextArticleIndex = currentArticleIndex + 1;
                                        if (nextArticleIndex > ($scope.feed.articles.length - 1)) {
                                            nextArticleIndex = $scope.feed.articles.length - 1 ;
                                        }
                                    }
                                    var nextArticle = $scope.feed.articles[nextArticleIndex];
                                    expandArticle(nextArticle, {
                                        switchCallback: function() {
                                            scrollTo.id('article-' + nextArticle.id);
                                        }
                                    });
                                }
                            }
                        }
                    }
            })
            .add({
                combo: 'right',
                description: 'Open preview block',
                action: 'keydown',
                callback: function () {
                    if (!articlesService.isFullTextOpened()) {
                        setViewTypePreview();
                    }
                }
            })
            .add({
                combo: 'left',
                description: 'Close preview block',
                action: 'keydown',
                callback: function () {
                    if (!articlesService.isFullTextOpened()) {
                        setViewTypeList();
                    }
                }
            })
            .add({
                combo: 's',
                description: 'Show full text',
                action: 'keydown',
                callback: function () {
                    if ($scope.selectedArticle) {
                        if (!articlesService.isFullTextOpened()) {
                            if ($scope.viewType !== VIEW_TYPE_PREVIEW) {
                                articlesService.openFullText($scope.selectedArticle);
                            }
                        } else {
                            articlesService.closeFullText();
                        }
                    }
                }
            });


            var _evalAsyncSelected;
            function expandArticle(article, options) {
                options = options || {};

                if ($scope.selectedArticle != article) {
                    if ($scope.selectedArticle) {
                        $scope.selectedArticle._isExpanded = false;
                        if (!$scope.selectedArticle.isRead) {
                            $scope.selectedArticle.isRead = true;
                        }
                    }
                    $scope.selectedArticle = article;
                    $scope.selectedArticle._isExpanded = true;
                }
                _evalAsyncSelected = article;
                if (options.switchCallback) {
                    $timeout(function() {
                        if (_evalAsyncSelected == article) {
                            options.switchCallback();
                        }
                    }, 0);
                }
                if (!article.isRead) {
                    article.viewsCount++;
                    feedsService.markArticleAsRead(article);
                    $scope.$emit('article:read', article, $scope.feed);
                }
                if ($scope.viewType === VIEW_TYPE_PREVIEW) {
                    setFullTextArticle(article)
                }

            }

            function reloadArticles(result) {

                loadCurrentPage = 1;
                $scope.viewType = VIEW_TYPE_LIST;
                $scope.feed = result.feed || {};

                $scope.pageLoading = false;
                $scope.selectedArticle = null;

                $scope.currentPage = loadCurrentPage;
                $scope.pageLoad = false;
                $scope.paginationEndReached = false;

                updateArticlesHtml(result.articles);
                $scope.feed.articles = result.articles;
            }

            function setViewTypePreview() {
                if ($scope.viewType !== VIEW_TYPE_PREVIEW) {
                    if ($scope.feed && $scope.feed.articles) {
                        if (!$scope.selectedArticle) {
                            $scope.selectedArticle = $scope.feed.articles[0];
                            $scope.selectedArticle._isExpanded = true;
                            if (!$scope.selectedArticle.isRead) {
                                feedsService.markArticleAsRead($scope.selectedArticle);
                                $scope.$emit('article:read', $scope.selectedArticle, $scope.feed);
                            }
                        }
                        openFullTextArticle($scope.selectedArticle);
                        $scope.viewType = VIEW_TYPE_PREVIEW;
                    }
                }
            }

            function setViewTypeList() {
                if ($scope.viewType !== VIEW_TYPE_LIST) {
                    closeFullTextArticle();
                    $scope.viewType = VIEW_TYPE_LIST;
                }
            }

            function openFullTextArticle(article) {
                isReadArticleAllowed = true;
                setFullTextArticle(article);
            }

            function closeFullTextArticle() {
                $scope.readArticle = null;
                if (readArticleCancelDef) {
                    readArticleCancelDef.resolve('closed');
                }
                isReadArticleAllowed = false;
            }

            function updateArticlesHtml(articles) {
                angular.forEach(articles, function(article) {
                    article.text = $sce.trustAsHtml(article.text)
                });
            }

            function setFullTextArticle(article) {
                if (!isReadArticleAllowed) {
                    isReadArticleAllowed = true;
                    return;
                }
                $scope.isReadArticleLoad = true;
                $scope.readArticle = {
                    article: article,
                    fullText: {}
                };
                if (readArticleCancelDef) {
                    readArticleCancelDef.resolve('cancelled');
                }
                readArticleLoadId = article.id;
                var req = feedsService.getFullArticleText(article.id);
                readArticleCancelDef = req.cancel;
                req.promise.then(function(res) {
                    if (!isReadArticleAllowed) {
                        isReadArticleAllowed = true;
                    } else if (readArticleLoadId == article.id) {
                        if (res.fullText) {
                            var fullText = res.fullText;
                            fullText.text = $sce.trustAsHtml(fullText.text);
                            $scope.readArticle = {
                                article: article,
                                fullText: fullText
                            };
                        }
                        $scope.isReadArticleLoad = false;
                    }
                }, function() {
                    if (!isReadArticleAllowed) {
                        isReadArticleAllowed = true;
                    }
                    if (readArticleLoadId == article.id) {
                        $scope.isReadArticleLoad = false;
                    }
                });

            }

        }
    ]);