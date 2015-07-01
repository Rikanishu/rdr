angular.module('rdr')
    .directive('rdrVisible', function() {
        return {
            restrict: 'A',
            link: function(scope, element, attr) {
                scope.$watch(attr.rdrVisible, function (visible) {
                    element.css('visibility', visible ? 'visible' : 'hidden');
                });
            }
        }
    });
