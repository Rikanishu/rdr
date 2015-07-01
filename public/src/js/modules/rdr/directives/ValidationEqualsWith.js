angular.module('rdr')
    .directive('rdrValidationEqualsWith', function() {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function(scope, element, attr, control) {
                var compareAttr = attr.rdrValidationEqualsWith;
                if (!compareAttr) {
                    throw new Error("Scope attribute is required");
                }
                var modelAttr = attr.ngModel;
                if (!modelAttr) {
                    throw new Error("Model attribute is required");
                }
                scope.$watch(compareAttr, function(value) {
                    var modelAttrValue = scope.$eval(modelAttr);
                    control.$setValidity('equals', (modelAttrValue === value));
                    return value;
                });
                control.$parsers.unshift(function(value) {
                    var currentScopeValue = scope.$eval(compareAttr);
                    control.$setValidity('equals', (currentScopeValue === value));
                    return value;
                })
            }
        }
    });