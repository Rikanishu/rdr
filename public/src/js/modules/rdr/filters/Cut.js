angular.module('rdr')
    .filter('cut', function() {
        return function(data, cutLength, replaceString) {
            if (angular.isUndefined(cutLength)) {
                throw new Error("Cut length (first parameter of filter cut) is required");
            }
            if (angular.isUndefined(replaceString)) {
                replaceString = "...";
            }

            if (data && data.length > cutLength) {
                data = data.slice(0, cutLength) + replaceString;
            }

            return data;
        }
    });
