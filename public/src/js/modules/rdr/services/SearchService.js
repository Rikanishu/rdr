angular.module('rdr')
    .factory('feedsSearchService', function($rootScope, $q, $http) {

        var Service = {};

        Service.search = function(options) {
            var def = $q.defer();
            $http.post('/feeds/articles/search', options).success(function(data) {
                def.resolve(data);
            }).error(function() {
                def.reject();
            });

            return def.promise;
        };

        return Service;

    });