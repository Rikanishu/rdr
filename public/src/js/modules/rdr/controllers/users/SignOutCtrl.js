angular.module('rdr')
    .controller('users.SignOutCtrl', [
        '$scope',
        '$state',
        'userAuthService',
        function($scope, $state, userAuthService) {
            userAuthService.quit().then(function() {
                $state.go('home');
            });
        }
    ]);
