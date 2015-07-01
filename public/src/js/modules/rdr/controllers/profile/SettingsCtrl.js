angular.module('rdr')
    .controller("profile.SettingsCtrl", [
        '$scope', '$state', 'userAuthService', 'userSettingsService', 'initData',
        function($scope, $state, userAuthService, userSettingsService, initData) {
            if (!userAuthService.isAuth()) {
                throw new Error('Run user settings controller without auth user');
            }

            $scope.user = userAuthService.user;
            $scope.settingsFormModel = {
                image: null,
                username: userAuthService.user.name
            };
            $scope.passwordFormModel = {
                oldPassword: '',
                newPassword: '',
                confirmNewPassword: ''
            };

            $scope.availableLanguages = initData.availableLanguages;
            $scope.sysSettingsModel = {
                language: initData.language
            };

            $scope.settingsFormSubmit = function(form) {
                if (form.$valid) {
                    userSettingsService.saveProfileSettings($scope.settingsFormModel).then(function(res) {
                        if (res.success) {
                            userAuthService.user.name = $scope.settingsFormModel.username;
                        }
                    });
                }
            };

            $scope.passwordChangeFormSubmit = function(form) {
                if (form.$valid) {
                    userSettingsService.changePassword($scope.passwordFormModel).then(function(res) {
                        $scope.passwordFormModel = {};
                        form.$setPristine();
                    }, function(res) {
                        if (!res.success) {
                            if (res.message == 'Invalid password') {
                                var field = form.oldPassword;
                                field.$remoteErrors = ['invalidOldPassword'];
                                field.$setValidity('invalidOldPassword', false);
                            }
                        }
                    });
                }
            };

            $scope.onSysSettingsChange = function() {
                userSettingsService.changeSystemSettings($scope.sysSettingsModel).then(function() {
                    location.reload();
                });
            };

            $scope.onImageUpload = function(res) {
                if (res.data && res.data.middle) {
                    $scope.user.imageSrc = res.data.middle;
                }
            };

            $scope.onSubscriptionsUploadStart = function() {
                $scope.isSubscriptionLoading = true;
            };

            $scope.onSubscriptionsUploadComplete = function(res) {
                $scope.isSubscriptionLoading = false;
            }
        }
    ]);

