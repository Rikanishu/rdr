angular.module('rdr')
    .controller('users.SignInCtrl', [
        '$scope',
        '$state',
        'userAuthService',
        function($scope, $state, userAuthService) {
            $scope.signIn = {};
            $scope.signInAction = function() {
                if ($scope.signIn.login && $scope.signIn.password) {
                    userAuthService.auth($scope.signIn.login, $scope.signIn.password).then(function() {
                        //$scope.signIn = {};
                        //$scope.signInForm.$setPristine();
                        $state.go('home');
                    }, function(reason) {
                        $scope.signIn.password = '';
                        $scope.signInError = 'Invalid login or password';
                    });
                } else {
                    $scope.signIn.password = '';
                    $scope.signInError = 'Login and password required';
                }
            }
        }
    ]);
