angular.module('rdr')
    .directive('rdrModal', function() {
        return {
            restrict: 'AE',
            link: function(scope, element, attr) {
                if (scope.modal) {
                    throw Error('Modal on scope already existed');
                }
                scope.modal = {};
                scope.modal.dismiss = function() {
                    element.modal('hide');
                }
            }
        }
    });
