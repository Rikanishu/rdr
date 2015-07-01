(function() {

    var format = function(string, args) {
        return string.replace(/{(\d+)}/g, function(match, number) {
            return (typeof args[number]) != 'undefined' ? args[number] : '';
        });
    };

    angular.module('rdr')
        .factory('l10n', [
            'initData',
            function(data) {
                var dictionary = data.l10nData || {};
                return function() {
                    var label = arguments[0];
                    if (!angular.isString(label)) {
                        return '';
                    }
                    /* hack for percent escape */
                    label = label.replace('%', '%%');
                    label = (label in dictionary) ? dictionary[label] : label;
                    label = label.replace('%%', '%');
                    var args = Array.prototype.slice.call(arguments, 1);
                    if (args.length) {
                        return format(label, args);
                    }
                    return label;
                }
            }
        ]);
}());
