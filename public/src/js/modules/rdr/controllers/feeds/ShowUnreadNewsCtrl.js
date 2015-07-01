angular.module('rdr')
    .controller("feeds.ShowUnreadNewsCtrl", [
        '$scope', '$state', '$controller', 'feedsService', 'l10n',
        function($scope, $state, $controller, feedsService, l10n) {

            $controller('feeds.ShowFeedCommonCtrl', {$scope: $scope, options: {
                searchCallback: function($state, $scope) {
                    $state.go('home.searchAll', {
                        'term': $scope.searchFormModel.query,
                        'type': 'unread',
                        'where': ['title', 'announce', 'text'].join(',')
                    });
                },
                loadCallback: function(page) {
                    return feedsService.getAllUnreadNews({page: page})
                },
                markAllAsReadCallback: function() {
                    var promise = feedsService.markAllUnreadAsRead();
                    promise.then(function() {
                        $scope.$emit('unread:readAll');
                    });
                    return promise;
                },
                cannotHaveUnread: false,
                cannotBeUpdated: true,
                cannotBeSubscribed: true
            }});

        }
    ]);