angular.module('rdr')
    .controller('users.SignUpCtrl', [
        '$scope',
        '$http',
        '$state',
        'userAuthService',
        function($scope, $http, $state, userAuthService) {
            /**
             * Called when form signup action triggered
             *
             * @param model
             * @param form
             */
            $scope.submit = function(model, form) {
                form.$submitted = true;
                if (form.$valid) {
                    $scope.showLoading = true;
                    $http.post('/users/signup', model).success(function(data) {
                        $scope.showLoading = false;
                        if (data) {
                            if (!data.success && data.errors) {
                                angular.forEach(data.errors, function(error, fieldName) {
                                    if (form[fieldName]) {
                                        var formControl = form[fieldName];
                                        var reason = error.reason || "serverError";
                                        formControl.$setValidity(reason, false);
                                        formControl.$remoteErrors = [reason];
                                    }
                                });
                            } else if (data.user) {
                                userAuthService.successSignup(data.user);
                                $state.go('home');
                            }
                        }
                    }).error(function() {
                        $scope.showLoading = false;
                    });
                }
            }
        }]
    );
