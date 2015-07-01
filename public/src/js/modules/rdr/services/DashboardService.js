angular.module('rdr')
    .factory('dashboardService', [
        '$q', '$http',
        function($q, $http) {

            var Service = {};

            Service.NEWS_TYPE_LASTVISIT = 'lastvisit';
            Service.NEWS_TYPE_POPULAR = 'popular';

            Service.getDashboardPageInfo = function() {
                var def = $q.defer();

                $http.get('/home/dashboard').success(function(data) {
                    def.resolve(data);
                }).error(function() {
                    def.reject();
                });

                return def.promise;
            };

            return Service;
        }
    ]);
