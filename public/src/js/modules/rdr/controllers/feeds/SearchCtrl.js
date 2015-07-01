angular.module('rdr')
    .controller("feeds.SearchCtrl", [
        '$scope', '$state', '$stateParams', '$sce', 'feedsSearchService', 'feedsService', 'articlesService',
        function($scope, $state, $stateParams, $sce, feedsSearchService, feedsService, articlesService) {

            var searchOptions = {};

            $scope.searchFormModel = {};
            $scope.isSearchForFeed = false;

            if ($stateParams.type) {
                searchOptions.type = $stateParams.type;
                $scope.searchFormModel.searchIn = searchOptions.type;
            }
            if ($stateParams.where) {
                searchOptions.where = $stateParams.where.split(',');
                $scope.searchFormModel.include = {};
                for (var i = 0, count = searchOptions.where.length; i < count; ++i) {
                    $scope.searchFormModel.include[searchOptions.where[i]] = true;
                }
            }

            searchOptions.query = $stateParams.term;
            searchOptions.page = 1;

            $scope.query = searchOptions.query;
            $scope.searchFormModel.query = searchOptions.query;

            if ($stateParams.feed) {
                searchOptions.feed = $stateParams.feed;
                $scope.isSearchForFeed = true;
            }

            $scope.pageLoading = true;
            if (searchOptions.feed) {
                feedsService.getFeedDetail(searchOptions.feed).then(function(res) {
                    if (res.feed) {
                        $scope.feed = res.feed;
                    }
                    showSearchResults();
                })
            } else {
                showSearchResults();
            }


            $scope.onSearchFormSubmit = function(e) {
                e.preventDefault();
                var include = [];
                angular.forEach($scope.searchFormModel.include, function(v, k) {
                    if (v) {
                        include.push(k)
                    }
                });
                if (include.length) {
                    if (searchOptions.feed) {
                        $state.go('home.searchFeed', {
                            'feed': searchOptions.feed,
                            'term': $scope.searchFormModel.query,
                            'type': $scope.searchFormModel.searchIn,
                            'where': include.join(',')
                        });
                    } else {
                        $state.go('home.searchAll', {
                            'term': $scope.searchFormModel.query,
                            'type': $scope.searchFormModel.searchIn,
                            'where': include.join(',')
                        });
                    }
                }
            };

            function showSearchResults() {
                feedsSearchService.search(searchOptions).then(function(data) {
                    $scope.feed = $scope.feed || {};
                    $scope.feed.articles = data.articles;
                    $scope.pageLoading = false;

                    $scope.loadMore = function() {
                        if (!$scope.paginationEndReached && !$scope.pageLoad) {
                            $scope.pageLoad = true;
                            $scope.paginationEndReached = true;
                            searchOptions.page++;
                            feedsSearchService.search(searchOptions).then(function(result) {
                                if (result.articles && result.articles.length) {
                                    $scope.feed.articles = $scope.feed.articles.concat(result.articles);
                                    $scope.paginationEndReached = false;
                                }
                            }).finally(function() {
                                $scope.pageLoad = false;
                            })
                        }
                    };

                    $scope.onAddToFavorites = function(article, e) {
                        e.preventDefault();
                        if (!article.isInFavorites) {
                            feedsService.addArticleToFavorites(article);
                        } else {
                            feedsService.removeArticleFromFavorites(article);
                        }
                    };

                    $scope.onArticleExpand = function(article) {
                        if ($scope.selectedArticle !== article) {
                            if ($scope.selectedArticle) {
                                $scope.selectedArticle._isExpanded = false;
                                if (!$scope.selectedArticle.isRead) {
                                    $scope.selectedArticle.isRead = true;
                                }
                            }
                            $scope.selectedArticle = article;
                            $scope.selectedArticle._isExpanded = true;
                        }
                        if (!article.isRead) {
                            feedsService.markArticleAsRead(article);
                            $scope.$emit('article:read', article, $scope.feed);
                        }
                    };

                    $scope.onReadArticle = function(article, e) {
                        e.preventDefault();
                        articlesService.openFullText(article);

                    };

                });
            }

        }
    ]);