angular.module('rdr')
    .filter('lang', function(l10n) {
        return function() {
            return l10n.apply(this, arguments);
        }
    });
