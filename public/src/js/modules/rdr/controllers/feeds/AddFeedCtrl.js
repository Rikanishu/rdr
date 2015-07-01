angular.module('rdr')
    .controller("feeds.AddFeedCtrl", [
        '$scope',
        '$state',
        'packageService',
        function($scope, $state, packageService) {
            packageService.getPopularPackages().then(function(data) {
                $scope.popularPackages = data.popularPackages;
            });
            $scope.onSubmit = function() {
                if ($scope.query) {
                    $scope.showLoading = true;
                    packageService.searchQuery($scope.query).then(function(data) {
                        if (data.success && data.packages) {
                            $scope.isSearched = true;
                            $scope.showLoading = false;
                            $scope.packages = data.packages;
                        }
                    });
                } else {
                    $scope.isSearched = false;
                }
            }
        }
    ]);