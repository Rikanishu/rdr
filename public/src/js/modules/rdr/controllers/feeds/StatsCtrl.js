angular.module('rdr')
    .controller("feeds.StatsCtrl", [
        '$scope', '$state', 'subscribesService', 'l10n',
        function($scope, $state, SubscribesService, l10n) {

            $scope.isLoading = true;
            $scope.statsData = [];
            $scope.statsTooltip = function(key, x, y, e, graph) {
                return '<p>' + parseInt(y) + ' ' + l10n('articles') + '</p>';
            };

            SubscribesService.getSubscribesStats().then(function(res) {
                $scope.isLoading = false;
                var statsData = [];
                if (res.stats) {
                    if (res.stats.graph) {
                        statsData.push({
                            name: "Overall",
                            data: fetchStatsSeries(res.stats.graph),
                            description: "Overall count for all subscribes"
                        });
                    }
                    $scope.statsGraphs = statsData;
                    $scope.subscriptionsCount = res.stats.subscriptionsCount;
                    $scope.readCount = res.stats.readCount || 0;
                    $scope.publishedCount = res.stats.publishedCount || 0;
                    $scope.favCount = res.stats.favCount || 0;

                    $scope.readingTable = res.stats.readingTable;
                    $scope.subscriptionsTable = res.stats.subscriptionsTable;
                }
            });

            function fetchStatsSeries(data) {
                var result = [
                    {
                        key: l10n('Read articles'),
                        values: []
                    },
                    {
                        key: l10n('Write articles'),
                        values: []
                    }
                ];
                for (var i = 0, count = data.length; i < count; ++i) {
                    result[0].values.push([data[i][0], data[i][1]]);
                    result[1].values.push([data[i][0], data[i][2]]);
                }
                return result
            }
        }
    ]);

