angular.module('rdr')
    .directive('rdrOnReachScrollTop', function() {
        return {
            restrict: 'AE',
            link: function(scope, $element, attr) {
                var rawElem = $element.get(0);
                var paddingHeight = scope.$eval(attr.paddingHeight);
                var paddingPercent = scope.$eval(attr.paddingPercent) || 5;
                //Warning: apply might be called many times in a short time
                $element.on('scroll', function() {
                    var offset = paddingHeight;
                    if (!offset) {
                        offset = rawElem.scrollHeight / 100.0 * paddingPercent;
                    }
                    if (rawElem.scrollTop <= offset) {
                        scope.$apply(attr.rdrOnReachScrollTop);
                        console.log('ScrollTop reached');
                    }
                })
            }
        }
    })
    .directive('rdrOnReachScrollBottom', function() {
        return {
            restrict: 'AE',
            link: function(scope, $element, attr) {
                var rawElem = $element.get(0);
                var paddingHeight = scope.$eval(attr.paddingHeight);
                var paddingPercent = scope.$eval(attr.paddingPercent) || 5;
                //Warning: apply might be called many times in a short time
                $element.on('scroll', function() {
                    var offset = paddingHeight;
                    if (!offset) {
                        offset = rawElem.scrollHeight / 100.0 * paddingPercent;
                    }
                    var pixelsDiff = Math.abs(rawElem.scrollHeight - (rawElem.scrollTop + rawElem.offsetHeight));
                    if (pixelsDiff <= offset) {
                        scope.$apply(attr.rdrOnReachScrollBottom);
                        console.log('ScrollBottom reached');
                    }
                })
            }
        }
    });