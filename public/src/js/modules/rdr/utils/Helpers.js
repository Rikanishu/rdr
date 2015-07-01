angular.module('rdr')
    .factory('helpers', function() {

        var idCounter = 0;
        var Helpers = {};

        Helpers.uniqueId = function(prefix) {
            var id = ++idCounter;
            return String(prefix == null ? '' : prefix) + id;
        };

        return Helpers;

    });
