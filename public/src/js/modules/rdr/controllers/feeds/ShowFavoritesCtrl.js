angular.module('rdr')
    .controller("feeds.ShowFavoritesCtrl", [
        '$scope', '$state', '$controller', 'feedsService', 'l10n',
        function($scope, $state, $controller, feedsService, l10n) {

            $controller('feeds.ShowFeedCommonCtrl', {$scope: $scope, options: {
                searchCallback: function($state, $scope) {
                    $state.go('home.searchAll', {
                        'term': $scope.searchFormModel.query,
                        'type': 'fav',
                        'where': ['title', 'announce', 'text'].join(',')
                    });
                },
                loadCallback: function(page) {
                    return feedsService.getFavoriteArticles({page: page})
                },
                markAllAsReadCallback: function() {
                    
                },
                cannotBeUpdated: true,
                cannotBeSubscribed: true,
                cannotHaveUnread: true
            }});

        }
    ]);