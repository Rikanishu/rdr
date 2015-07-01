angular.module('rdr')
    .directive('rdrValidationRemote', function() {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function(scope, element, attr, control) {
                element.on('change blur', function() {
                    if (control.$remoteErrors && control.$remoteErrors.length) {
                        angular.forEach(control.$remoteErrors, function(err) {
                            control.$setValidity(err, true);
                        });
                        control.$remoteErrors = [];
                    }
                })
            }
        }
    });