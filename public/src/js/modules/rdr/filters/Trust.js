angular.module('rdr')
    .filter('trust', function($sce) {
        return function(text) {
            return $sce.trustAsHtml(text);
        }
    });
