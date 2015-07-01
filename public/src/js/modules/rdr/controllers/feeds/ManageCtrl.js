angular.module('rdr')
    .controller("feeds/ManageCtrl", [
        '$rootScope', '$scope', '$state', 'subscribesService', 'l10n',
        function($rootScope, $scope, $state, subscribesService, l10n) {

            $scope.commands = [];

            subscribesService.getSubscribesList().then(function(result) {
                $scope.rootSubscribes = [];
                $scope.folders = [];
                angular.forEach(result.subscribes, function(sub) {
                    if (sub.type === subscribesService.SUBSCRIBE_FOLDER) {
                        $scope.folders.push(sub);
                    } else {
                        $scope.rootSubscribes.push(sub);
                    }
                });
            });

            $scope.onSave = function() {
                var data = {
                    rootSubscribes: [],
                    folders: []
                };
                var i, count;
                angular.forEach($scope.rootSubscribes, function(sub) {
                    data.rootSubscribes.push({
                        name: sub.name,
                        feedId: sub.feedId
                    });
                });
                angular.forEach($scope.folders, function(folder) {
                    var folderData = {
                        name: folder.name,
                        feeds: []
                    };
                    angular.forEach(folder.feeds, function(sub) {
                        folderData.feeds.push({
                            name: sub.name,
                            feedId: sub.feedId
                        });
                    });
                    data.folders.push(folderData);
                });

                subscribesService.saveSubscribes(data);
                $rootScope.$emit('subscribes:refresh');
                $state.go('home');
            };

            $scope.onBack = function() {
                $state.go('home');
            };

            $scope.onRevert = function() {
                if ($scope.commands.length) {
                    $scope.commands.pop().revert();
                }
            };

            $scope.onFolderEdit = function(folder) {
                if (folder._isEdit) {
                    if (folder.name !== '') {
                        folder._isEdit = false;
                    }
                } else {
                    folder._isEdit = true;
                }
            };

            $scope.onFolderRemove = function(folder) {
                var command = new DeleteFolderCommand(folder);
                command.run();
                $scope.commands.push(command);
            };

            $scope.onSubscriptionRemove = function(sub, e) {
                e.stopPropagation();
                e.preventDefault();
                var command = new DeleteSubscriptionCommand(sub);
                command.run();
                $scope.commands.push(command);
            };

            $scope.onFolderNameChange = function(folder) {
                if (folder.name !== '') {
                    folder._isEdit = false;
                }
            };

            $scope.onAddFolder = function() {
                $scope.folders.push({
                    active: true,
                    name: '',
                    type: 'folder',
                    parentId: 0,
                    _isEdit: true,
                    _isNew: true
                })
            };

            $scope.onDropInRoot = function(droppedSubscribe, e) {
                deleteFromSubscribes(droppedSubscribe);
                $scope.rootSubscribes.push(droppedSubscribe);
            };

            $scope.onDropInRootSubscription = function(currentSubscribe, droppedSubscribe, e) {
                if (currentSubscribe.id != droppedSubscribe.id) {
                    deleteFromSubscribes(droppedSubscribe);
                    if (!$scope.rootSubscribes || !$scope.rootSubscribes.length) {
                        $scope.rootSubscribes = [droppedSubscribe];
                    } else {
                        var currentIndex = $scope.rootSubscribes.indexOf(currentSubscribe);
                        if (currentIndex != -1) {
                            $scope.rootSubscribes = [].concat(
                                $scope.rootSubscribes.slice(0, currentIndex),
                                [droppedSubscribe],
                                $scope.rootSubscribes.slice(currentIndex)
                            );
                        }
                    }
                }
            };

            $scope.onDropInFolder = function(folder, droppedSubscribe, e) {
                deleteFromSubscribes(droppedSubscribe);
                if (!folder.feeds) {
                    folder.feeds = [droppedSubscribe];
                } else {
                    folder.feeds.push(droppedSubscribe);
                }
            };

            $scope.onDropInFolderSubscription = function(currentSubscribe, folder, droppedSubscribe, e) {
                if (currentSubscribe.id != droppedSubscribe.id) {
                    deleteFromSubscribes(droppedSubscribe);
                    $scope.$digest();
                    if (!folder.feeds || !folder.feeds.length) {
                        folder.feeds = [droppedSubscribe];
                    } else {
                        var currentIndex = folder.feeds.indexOf(currentSubscribe);
                        if (currentIndex != -1) {
                            folder.feeds = [].concat(
                                folder.feeds.slice(0, currentIndex),
                                [droppedSubscribe],
                                folder.feeds.slice(currentIndex)
                            );
                        }
                    }
                }
            };

            function deleteFromSubscribes(subscribe) {
                var index = $scope.rootSubscribes.indexOf(subscribe);
                var deleted = false;
                var subscribeFolder = null;
                if (index != -1) {
                    $scope.rootSubscribes.splice(index, 1);
                    deleted = true;
                } else {
                    angular.forEach($scope.folders, function(folder) {
                        if (folder.feeds && folder.feeds.length) {
                            index = folder.feeds.indexOf(subscribe);
                            if (index != -1) {
                                folder.feeds.splice(index, 1);
                                subscribeFolder = folder;
                                deleted = true;
                            }
                        }
                    });
                }

                return {
                    deleted: deleted,
                    index: index,
                    folder: subscribeFolder
                }
            }

            function deleteFromFolders(folder) {
                var index = $scope.folders.indexOf(folder);
                var deleted = false;
                if (index != -1) {
                    $scope.folders.splice(index, 1);
                    deleted = true;
                }

                return {
                    index: index,
                    deleted: deleted
                }

            }

            function DeleteSubscriptionCommand(subscription) {

                var executedResult = {};
                var command = {};
                command.title = l10n('Subscription delete');
                command.run = function() {
                    executedResult = deleteFromSubscribes(subscription)
                };
                command.revert = function() {
                    if (executedResult.deleted) {
                        if (executedResult.folder) {
                            var folder = executedResult.folder;
                            if (folder.feeds.length > executedResult.index) {
                                folder.feeds = [].concat(
                                    folder.feeds.slice(0, executedResult.index),
                                    [subscription],
                                    folder.feeds.slice(executedResult.index)
                                );
                            } else {
                                folder.feeds.push(subscription)
                            }
                        } else {
                            if ($scope.rootSubscribes.length > executedResult.index) {
                                $scope.rootSubscribes = [].concat(
                                    $scope.rootSubscribes.slice(0, executedResult.index),
                                    [subscription],
                                    $scope.rootSubscribes.slice(executedResult.index)
                                );
                            } else {
                                $scope.rootSubscribes.push(subscription);
                            }
                        }
                    }
                };

                return command;
            }

            function DeleteFolderCommand(folder) {

                var command = {};
                command.title = l10n('Folder delete');
                command.run = function() {
                    deleteFromFolders(folder);
                };
                command.revert = function() {
                    $scope.folders.push(folder);
                };

                return command;
            }
        }
    ]);