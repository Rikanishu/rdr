angular.module('rdr')
    .directive('rdrSubscriberNewFolder', function() {
        return {
            restrict: 'A',
            link: function(scope, $element, attr) {
                var item = scope.$eval(attr.rdrSubscriberNewFolder);
                var $form = $element.closest('form');
                var creationCanceled = false;
                var cancel = function() {
                    if (scope.cancelNewFolderCreation && angular.isFunction(scope.cancelNewFolderCreation)) {
                        scope.cancelNewFolderCreation(item);
                    }
                };

                $element.on('blur', function() {
                    if (!creationCanceled) {
                        if ($element.val() !== '') {
                            $form.submit();
                        } else {
                            cancel();
                        }
                    }
                });

                $form.find('.cancel-icon').on('click', function(e) {
                    e.stopPropagation();
                    e.preventDefault();
                    creationCanceled = true;
                    cancel();
                });

                $form.on('submit', function(e) {
                   if ($element.val() == '') {
                       e.preventDefault();
                   }
                });

                $element.focus();
            }
        }
    });
