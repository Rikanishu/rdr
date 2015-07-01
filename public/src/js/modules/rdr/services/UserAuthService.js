angular.module('rdr')
    .factory('userAuthService', [
        '$rootScope', '$http', '$q', '$interval', 'initData',
        function($rootScope, $http, $q, $interval, initData) {

            var ACTIVITY_CHECKING_TIMEOUT = 300;

            var Service = {};

            Service.user = initData.user || null;

            Service.auth = function(login, password) {
                if (this.isAuth()) {
                    throw new Error("User already logged")
                }

                var def = $q.defer();
                var self = this;
                var req = {
                    login: login,
                    password: password
                };

                $http.post('/users/auth', req).success(function(data) {
                    if (data.success && data.user) {
                        self.user = data.user;
                        $rootScope.$emit('user:auth', self.user);
                        def.resolve(self.user, self);
                    } else {
                        $rootScope.$emit('user:invalidAuth', req);
                        def.reject();
                    }
                }).error(function() {
                    $rootScope.$emit('user:invalidAuth', req);
                    def.reject();
                });

                return def.promise;
            };

            Service.quit = function() {
                var def = $q.defer();
                var self = this;
                if (self.user) {
                    var exitedUser = self.user;
                    self.user = null;

                    $http.post('/users/quit').success(function(data) {
                        def.resolve(exitedUser);
                        $rootScope.$emit('user:quit', exitedUser);
                    });
                } else {
                    def.resolve(null);
                }

                return def.promise;
            };

            Service.isAuth = function() {
                return (this.user !== null && this.user.type !== "anon");
            };

            Service.successSignup = function(user) {
                this.user = user;
                $rootScope.$emit('user:auth', this.user);
                return this.isAuth();
            };

            Service.runActivityChecking = function() {
                $interval(function() {
                    $http.post('/users/activity-checking');
                }, ACTIVITY_CHECKING_TIMEOUT * 1000);
            };

            return Service;
    }]);
