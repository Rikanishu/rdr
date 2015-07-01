angular.module('rdr')
    .controller("feeds.ShowFeedCtrl", [
        '$rootScope', '$scope', '$state', '$stateParams', '$controller', 'feedsService',
        function($rootScope, $scope, $state, $stateParams, $controller, feedsService) {

            var feedId = parseInt($stateParams.feedId);
            if (feedId < 1) {
                throw new Error("Invalid feed id");
            }

            $scope.$emit('feeds:showList', feedId);

            $controller('feeds.ShowFeedCommonCtrl', {$scope: $scope, options: {
                loadCallback: function(page) {
                    return feedsService.getArticles(feedId, {page: page});
                }
            }});
        }
    ]);