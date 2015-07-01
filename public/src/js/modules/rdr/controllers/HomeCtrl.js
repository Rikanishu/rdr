angular.module('rdr')
    .controller("HomeCtrl", [
        '$rootScope', '$scope', '$state', 'userAuthService',
        function($rootScope, $scope, $state, userAuthService) {
            $scope.leftSideBlockCollapsed = true;
            $scope.toggleCollapseLeftSideBlock = function() {
                $scope.leftSideBlockCollapsed = !$scope.leftSideBlockCollapsed;
            };
            $scope.hideSubstrate = function() {
                $scope.leftSideBlockCollapsed = true;
            };
            $scope.user = userAuthService.user;
        }

    ]);