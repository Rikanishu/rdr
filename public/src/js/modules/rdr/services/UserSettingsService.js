angular.module('rdr')
    .factory('userSettingsService', [
        '$q', '$http',
        function($q, $http) {

            var Service = {};

            Service.saveProfileSettings = function(settings) {
                var def = $q.defer();
                $http.post('/users/settings/change-profile-settings', settings)
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function(response) {
                        def.reject(response);
                    });
                return def.promise;
            };

            Service.changeSystemSettings = function(settings) {
                var def = $q.defer();
                $http.post('/users/settings/lang-change', settings)
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function(response) {
                        def.reject(response);
                    });
                return def.promise;
            };

            Service.changePassword = function(settings) {
                var def = $q.defer();
                $http.post('/users/settings/change-password', settings)
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