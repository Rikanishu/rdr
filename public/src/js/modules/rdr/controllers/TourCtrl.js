angular.module('rdr')
    .controller("TourCtrl", function($scope, $state, $q, $timeout) {
        $state.go('signin');
    });
