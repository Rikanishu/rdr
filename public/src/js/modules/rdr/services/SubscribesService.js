angular.module('rdr')
    .factory('subscribesService', [
        '$q', '$http',
        function($q, $http) {

            var Service = {};

            Service.SUBSCRIBE_FOLDER = 'folder';
            Service.SUBSCRIBE_FEED = 'feed';

            Service.getSubscribesList = function() {
                var def = $q.defer();
                $http.get('/subscribes/list').success(function(data) {
                    def.resolve(data);
                }).error(function() {
                    def.reject();
                });

                return def.promise;
            };

            Service.createNewFolder = function(folderInfo) {
                var def = $q.defer();
                $http.post('/subscribes/create-folder', {
                    name: folderInfo.name
                }).success(function(data) {
                    def.resolve(data);
                }).error(function() {
                    def.reject();
                });

                return def.promise;
            };

            Service.newSubscribe = function(subscribeInfo) {
                var def = $q.defer();
                $http.post('/subscribes/new-subscribe', subscribeInfo).success(function(data) {
                    def.resolve(data);
                }).error(function() {
                    def.reject();
                });

                return def.promise;
            };

            Service.getSubscribesStats = function() {
                var def = $q.defer();
                $http.get('/subscribes/stats').success(function(data) {
                    def.resolve(data);
                }).error(function() {
                    def.reject();
                });

                return def.promise;
            };

            Service.saveSubscribes = function(subscribes) {
                var def = $q.defer();
                $http.post('/subscribes/save', subscribes).success(function(data) {
                    def.resolve(data);
                }).error(function() {
                    def.reject();
                });

                return def.promise;
            };

            return Service;
        }
    ]);
