angular.module('rdr')
    .directive('rdrBgImg', function() {
        return {
            restrict: 'A',
            link: function (scope, $element, attr) {
                var url = attr.rdrBgImg;
                if (url) {
                    $element.css({
                        'background-image': 'url(' + url + ')'
                    });
                }
            }
        }
    });
