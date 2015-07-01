angular.module('rdr')
    .controller("IndexCtrl", [
        '$scope', '$state', 'userAuthService',
        function($scope, $state, userAuthService) {
            if (!userAuthService.user) {
                return $state.go('tour');
            }
            return $state.go('home');
        }
    ]);

