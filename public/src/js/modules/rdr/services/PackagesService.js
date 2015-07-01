angular.module('rdr')
    .factory('packageService', function($rootScope, $q, $http) {

        var Service = {};

        Service.searchQuery = function(query) {
            var def = $q.defer();
            $http.post('/feeds/packages/resolve', {
                'query': query
            }).success(function(data) {
                def.resolve(data);
            }).error(function() {
                def.reject();
            });

            return def.promise;
        };

        Service.getPopularPackages = function() {
            var def = $q.defer();

            $http.get('/feeds/packages/popular').success(function(data) {
                def.resolve(data);
            }).error(function() {
                def.reject();
            });

            return def.promise;
        };

        return Service;

    });