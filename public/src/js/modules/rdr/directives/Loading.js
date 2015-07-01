angular.module('rdr')
    .directive('rdrLoading', [
        '$timeout', 'l10n', 'helpers',
        function($timeout, l10n, helpers) {
            return {
                restrict: 'A',
                link: function (scope, $element, attr) {

                    var titleText = attr.rdrLoadingTitle || l10n("Loading...");
                    var messageText = attr.rdrLoadingMessage || l10n("Please wait while application loading");
                    var displayingDelay = attr.rdrLoadingDisplayingDelay || 0;

                    var overlayId = "loadingOverlay_" + helpers.uniqueId();

                    scope.$watch(attr.rdrLoading, function(value) {
                        var $overlay = $element.find('#' + overlayId);
                        var hasOverlay = ($overlay.length > 0);
                        if (value) {
                            if (!hasOverlay) {
                                $element.children().hide();
                                $timeout(function() {
                                    var $overlayRoot = $('<div>')
                                        .attr('id', overlayId)
                                        .addClass('rdr-loading-overlay');
                                    var $spinnerElement = $('<div>')
                                        .addClass('rdr-loading-spinner');
                                    var $spinnerImage = $('<img>')
                                        .attr('src', 'static/img/common/spinner.gif');
                                    $overlayRoot.append($('<h4>').text(titleText));
                                    $overlayRoot.append($('<p>').text(messageText));
                                    $spinnerElement.append($spinnerImage);
                                    $overlayRoot.append($spinnerElement);
                                    $element.append($overlayRoot);
                                }, displayingDelay);
                            }
                        } else {
                            if (hasOverlay) {
                                $overlay.remove();
                                $element.children().show();
                            }
                        }
                    });
                }
            }
        }
    ]);
