angular.module('rdr')
    .controller("feeds.OfflineQueueCtrl", [
        '$scope', '$state', '$timeout', 'offlineReadQueueService',
        function($scope, $state, $timeout, offlineReadQueueService) {

            $scope.isLoading = true;
            $scope.isGenerationProcess = false;
            $scope.saveModel = {
                saveType: 'download',
                fileFormat: 'pdf'
            };
            offlineReadQueueService.getOfflineQueueArticles().then(function(res) {
                $scope.articles = res.articles;
                $scope.isLoading = false;

                $scope.removeFromQueue = function(article, e) {
                    e.preventDefault();
                    offlineReadQueueService.removeArticleFromQueue(article.id);
                    var index = $scope.articles.indexOf(article);
                    if (index !== -1) {
                        $scope.articles.splice(index, 1);
                    }
                };

                $scope.saveAction = function(e) {
                    $scope.isGenerationProcess = true;
                    e.preventDefault();
                    offlineReadQueueService.generateFile({
                        format: $scope.saveModel.fileFormat
                    }).then(function(res) {
                        var taskId = res.taskId;
                        var onResolved = function() {
                            $scope.isGenerationProcess = false;
                            if ($scope.saveModel.saveType === 'download') {
                                offlineReadQueueService.downloadGeneratedFile(taskId);
                            }
                        };
                        var checkStatus = function() {
                            $timeout(function() {
                                offlineReadQueueService.checkTaskCompleted(taskId).then(function(res) {
                                    if (res.isCompleted) {
                                        onResolved();
                                    } else {
                                        checkStatus();
                                    }
                                }, function() {
                                    checkStatus();
                                })
                            }, 500);
                        };
                        checkStatus();
                    });
                };
            });

            $scope.clearQueue = function(e) {
                e.preventDefault();
                offlineReadQueueService.clearQueue().then(function() {
                    $scope.articles = [];
                });
            }

        }
    ]);