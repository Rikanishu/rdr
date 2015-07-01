angular.module('rdr')
    .factory('offlineReadQueueService', [
        '$q', '$http',
        function($q, $http) {

            var Service = {};

            Service.addArticleToQueue = function(articleId) {
                var def = $q.defer();
                $http.post('/feeds/offline-read-queue/add-article', { articleId: articleId })
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function(response) {
                        def.reject(response);
                    });
                return def.promise;
            };

            Service.removeArticleFromQueue = function(articleId) {
                var def = $q.defer();
                $http.post('/feeds/offline-read-queue/remove-article', { articleId: articleId })
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function(response) {
                        def.reject(response);
                    });
                return def.promise;
            };


            Service.addFeedUnreadToQueue = function(feedId) {
                var def = $q.defer();
                $http.post('/feeds/offline-read-queue/add-feed-unread', { feedId: feedId })
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function(response) {
                        def.reject(response);
                    });
                return def.promise;
            };

            Service.getOfflineQueueArticles = function(options) {
                var def = $q.defer();
                var requestParams = {};
                if (options) {
                    if (options.page) {
                        requestParams.page = options.page;
                    }
                }
                $http.get('/feeds/offline-read-queue/list', {params: requestParams})
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function() {
                        def.reject();
                    });

                return def.promise;
            };

            Service.generateFile = function(options) {
                var def = $q.defer();
                var requestParams = {};
                if (options) {
                    if (options.format) {
                        requestParams.format = options.format;
                    }
                }
                $http.post('/feeds/offline-read-queue/generate-file', requestParams)
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function() {
                        def.reject();
                    });

                return def.promise;
            };

            Service.checkTaskCompleted = function(taskId) {
                var def = $q.defer();
                $http.get('/feeds/offline-read-queue/check-task-completed/' + taskId)
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function() {
                        def.reject();
                    });

                return def.promise;
            };

            Service.downloadGeneratedFile = function(taskId) {
                window.location = '/feeds/offline-read-queue/download-file/' + taskId;
            };

            Service.clearQueue = function() {
                var def = $q.defer();
                $http.post('/feeds/offline-read-queue/clear-queue')
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function(response) {
                        def.reject(response);
                    });
                return def.promise;
            };

            return Service;
        }
    ]);