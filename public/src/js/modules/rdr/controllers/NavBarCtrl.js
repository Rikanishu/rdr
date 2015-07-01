angular.module('rdr')
    .controller('NavBarCtrl', [
        '$rootScope', '$scope', 'userAuthService', 'initData',
        function($rootScope, $scope, userAuthService, initData) {
            $scope.user = userAuthService.user;
            $rootScope.$on('user:auth', function(e, newUser) {
                $scope.user = newUser
            });
            $rootScope.$on('user:quit', function() {
                $scope.user = null;
            });

            $scope.isSigninEnabled = true;
            $scope.isSignupEnabled = initData.appOptions.isSignupEnabled;
        }
    ]);