angular.module('rdr')
    .directive('rdrReadArticleToggle', [
        '$animate', '$timeout', '$q',
        function($animate, $timeout, $q) {
            return {
                restrict: 'A',
                link: function(scope, element, attr) {

                    var _prevAnimDef;
                    scope.$watch('viewType', function(viewType) {
                        if (_prevAnimDef) {
                            _prevAnimDef.reject();
                        }
                        var def = $q.defer();
                        _prevAnimDef = def;
                        if (viewType === 'preview') {
                            element.removeClass('without-preview');
                            element.addClass('with-preview');
                            $animate.addClass(element, 'show-preview');
                            def.promise.then(function() {
                                element.addClass('prev-complete');
                            });
                            $timeout(function() {
                                def.resolve();
                            }, 800);
                        } else if (viewType === 'list') {
                            element.removeClass('prev-complete');
                            $animate.removeClass(element, 'show-preview');
                            def.promise.then(function() {
                                element.removeClass('with-preview');
                                element.addClass('without-preview');
                            });
                            $timeout(function() {
                                def.resolve();
                            }, 800);
                        }
                    });
                }
            }
        }
    ]);
