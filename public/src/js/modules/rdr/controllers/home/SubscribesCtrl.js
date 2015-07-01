angular.module('rdr')
    .controller("home.SubscribesCtrl", [
        '$rootScope', '$scope', '$state', '$q', 'subscribesService',
        function($rootScope, $scope, $state, $q, subscribesService) {

            /**
             * All subscribes list. Not used in template.
             * @type {Array}
             */
            $scope.subscribes = [];

            /**
             * Current selected subscribe
             * @type {null}
             */
            $scope.selectedSubscribe = null;

            /**
             * Total count of unread articles
             * @type {number}
             */
            $scope.totalUnreadCount = 0;

            /**
             * Subscriptions sorted by types
             * Used in templates
             *
             * @type {{subscriptions: Array, folders: Array}}
             */
            $scope.subscribesByType = {
                subscriptions: [],
                folders: []
            };

            var loadPromise = refreshSubscribes();

            $scope.onAllNewsSelect = function() {
                resetSelectedSubscribe();
                $state.go('home.unreadNews');
            };

            $scope.onFavoritesSelect = function() {
                resetSelectedSubscribe();
                $state.go('home.favorites');
            };

            $scope.onNewFolderClick = function() {
                createNewFolder();
            };

            $scope.onNewFolderCreate = function(item, model) {
                if (model.name) {
                    item.name = model.name;
                    subscribesService.createNewFolder(item).then(function(result) {
                        var subscribeItem = result.subscribe;
                        angular.forEach(subscribeItem, function(v, k) {
                            item[k] = v;
                        });
                        if (!item.feeds) {
                            item.feeds = []
                        }
                        item._isNew = false;
                        item._isSelected = false;
                    });
                }
            };

            $scope.onDropInFolder = function(folder, pkg, e) {
                if (checkPackage(pkg) && !pkg.isSubscribed) {
                    subscribesService.newSubscribe({
                        packageId: pkg.id,
                        packageType: pkg.type,
                        folder: folder.id
                    }).then(function(result) {
                        folder._isSelected = true;
                        addSubscribeToFolder(result.subscribe, folder);
                        pkg.isSubscribed = true;
                        pkg.subscribedCount++;
                        $scope.totalUnreadCount = result.totalUnreadCount;
                    });
                }

            };

            $scope.onDropInRoot = function(data, e) {
                if (checkPackage(data) && !data.isSubscribed) {
                    subscribesService.newSubscribe({
                        packageId: data.id,
                        packageType: data.type,
                        folder: 0
                    }).then(function(result) {
                        addSubscribe(result.subscribe);
                        data.isSubscribed = true;
                        data.subscribedCount++;
                        $scope.totalUnreadCount = result.totalUnreadCount;
                    });
                }

            };

            $scope.onDropInNewFolder = function(data, e) {
                console.log('Drop in new folder:', data);
            };

            $scope.cancelNewFolderCreation = cancelNewFolderCreation;

            $rootScope.$on('feeds:showList', function(e, feedId) {
                var handler = function() {
                    if (!$scope.selectedSubscribe) {
                        selectSubscribeFeed(feedId)
                    }
                };
                if (loadPromise) {
                    loadPromise.then(handler);
                } else {
                    handler();
                }
            });

            $rootScope.$on('article:read', function(e, article, feed) {
                if (feed.id) {
                    angular.forEach($scope.subscribes, function(sub) {
                        if (sub.feeds && sub.feeds.length) {
                            angular.forEach(sub.feeds, function(sub) {
                                if (sub.feedId == feed.id && sub.unreadCount > 0) {
                                    sub.unreadCount--;
                                }
                            });
                        }
                        if (sub.feedId == feed.id && sub.unreadCount > 0) {
                            sub.unreadCount--;
                        }
                    });
                }
                if ($scope.totalUnreadCount > 0) {
                    $scope.totalUnreadCount--;
                }
            });

            $rootScope.$on('unread:readAll', function() {
                angular.forEach($scope.subscribes, function(toplevel) {
                    if (toplevel.feeds && toplevel.feeds.length) {
                        angular.forEach(toplevel.feeds, function(sub) {
                            if (sub.feedId == feed.id && sub.unreadCount > 0) {
                                sub.unreadCount = 0;
                            }
                        });
                    } else {
                        toplevel.unreadCount = 0;
                    }
                });
                if ($scope.totalUnreadCount > 0) {
                    $scope.totalUnreadCount = 0;
                }
            });

            $rootScope.$on('subscribes:refresh', function(e, opts) {
                refreshSubscribes().then(function() {
                    if (opts && opts.active) {
                        selectSubscribeFeed(opts.active.id);
                    }
                });
            });

            function selectSubscribeFeed(feedId) {
                if ($scope.subscribes) {
                    angular.forEach($scope.subscribes, function(parent) {
                        if (parent.feeds && parent.feeds.length) {
                            angular.forEach(parent.feeds, function(sub) {
                                if (sub.feedId == feedId) {
                                    $scope.selectedSubscribe = sub;
                                    $scope.selectedSubscribe._isSelected = true;
                                    parent._isSelected = true;
                                    return false;
                                }
                            });
                        } else {
                            if (parent.feedId == feedId) {
                                $scope.selectedSubscribe = parent;
                                $scope.selectedSubscribe._isSelected = true;
                                return false;
                            }
                        }
                    })
                }
            }

            function isInFolder(subscribesFolder, subscribe) {
                for (var i = 0, count = subscribesFolder.feeds.length; i < count; ++i) {
                    if (subscribesFolder.feeds[i] === subscribe) {
                        return true;
                    }
                }
                return false;
            }

            function createNewFolder() {
                var folder = {
                    type: 'folder',
                    _isNew: true
                };
                $scope.subscribesByType.folders.push(folder);
            }

            function cancelNewFolderCreation(item) {
                var index = $scope.subscribesByType.folders.indexOf(item);
                if (index !== -1) {
                    $scope.subscribesByType.folders.splice(index, 1);
                    $scope.$apply();
                }
            }

            function resetSelectedSubscribe() {
                if ($scope.selectedSubscribe) {
                    $scope.selectedSubscribe._isSelected = false;
                    $scope.selectedSubscribe = null;
                }
            }

            function checkPackage(pkg) {
                return (pkg && pkg.hasOwnProperty('url') && pkg.hasOwnProperty('type'));
            }

            function addSubscribe(item) {
                $scope.subscribes.push(item);
                if (item.type === 'folder') {
                    $scope.subscribesByType.folders.push(item);
                } else {
                    $scope.subscribesByType.subscriptions.push(item);
                }
            }

            function addSubscribeToFolder(item, folder) {
                folder.feeds.push(item);
            }

            function refreshSubscribes() {
                var def = $q.defer();
                var loadPromise = def.promise;
                $scope.showLoading = true;
                subscribesService.getSubscribesList().then(function(result) {
                    var subscribes = result.subscribes;

                    angular.forEach(subscribes, function(item) {
                        item._isSelected = false;
                    });

                    $scope.showLoading = false;
                    $scope.subscribes = subscribes;

                    $scope.subscribesByType.folders = [];
                    $scope.subscribesByType.subscriptions = [];
                    angular.forEach(subscribes, function(item) {
                        if (item.type === 'folder') {
                            $scope.subscribesByType.folders.push(item);
                        } else {
                            $scope.subscribesByType.subscriptions.push(item);
                        }
                    });

                    $scope.totalUnreadCount = result.totalUnreadCount;
                    $scope.selectedSubscribe = null;

                    $scope.onSubscribeFolderSelect = function(item) {
                        item._isSelected = !item._isSelected;
                    };

                    $scope.onSubscribeSelect = function(item) {
                        if (item.type === subscribesService.SUBSCRIBE_FOLDER) {
                            throw new Error("Selected subscribe must be feed");
                        }

                        if ($scope.selectedSubscribe) {
                            $scope.selectedSubscribe._isSelected = false;
                        }
                        item._isSelected = true;
                        $scope.selectedSubscribe = item;
                        $state.go('home.showFeed', {
                            feedId: item.feedId
                        });
                    };

                    def.resolve();
                });

                return loadPromise;
            }
        }
    ]);