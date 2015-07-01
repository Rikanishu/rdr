angular.module('rdr')
    .factory('scrollTo', function($window, $document) {

        var ScrollTo = {};

        ScrollTo.top = function() {
            $window.scrollTo(0, 0);
        };

        ScrollTo.id = function(elementId, options) {
            ScrollTo.elem($document.find('#' + elementId), options);
        };

        ScrollTo.elem = function($elem, options) {
            options = angular.extend({
                focus: true,
                offset: 0
            }, options);
            if ($elem.length) {
                var elem = $elem.get(0);
                if (options.focus) {
                    elem.focus = true;
                }
                var $container = $elem.closest('[rdr-scroll-to-container]');
                if ($container.length) {
                    $container.scrollTop(elem.offsetTop - options.offset)
                } else {
                    if (options.offset) {
                        var top = $elem.offset().top - options.offset;
                        $window.scrollTo(0, top);
                    } else {
                        elem.scrollIntoView();
                    }
                }
            }
        };

        return ScrollTo;

    });