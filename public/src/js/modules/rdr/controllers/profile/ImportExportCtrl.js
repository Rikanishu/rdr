angular.module('rdr')
    .controller("profile.ImportExportCtrl", [
        '$scope', '$state', 'userAuthService',
        function($scope, $state) {

            $scope.onSubscriptionsUploadStart = function() {
                $scope.isSubscriptionLoading = true;
            };

            $scope.onSubscriptionsUploadComplete = function(res) {
                $scope.isSubscriptionLoading = false;
            }
        }
    ]);

