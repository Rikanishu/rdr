angular.module('rdr')
    .controller("home.DashboardCtrl", [
        '$scope', '$state', 'dashboardService', 'articlesService',
        function($scope, $state, dashboardService, articlesService) {

            $scope.isDashboardLoaded = false;
            dashboardService.getDashboardPageInfo().then(function(data) {
                if (data.news) {
                    $scope.newsFirstLine = data.news.slice(0, 3);
                    $scope.newsOthers = data.news.slice(3);
                    $scope.isLastVisitNews = (data.type === dashboardService.NEWS_TYPE_LASTVISIT);
                    $scope.isPopularNews = (data.type === dashboardService.NEWS_TYPE_POPULAR);
                    $scope.isDashboardLoaded = true;
                }
            });

            $scope.searchFormModel = {
                query: '',
                searchIn: 'all',
                include: {
                    title: true,
                    announce: true,
                    text: true
                }
            };

            $scope.openArticlePreview = function(article, e) {
                e.preventDefault();
                articlesService.openFullText(article);
            };

            $scope.onSearchFormSubmit = function(e) {
                e.preventDefault();
                var include = [];
                angular.forEach($scope.searchFormModel.include, function(v, k) {
                    if (v) {
                        include.push(k)
                    }
                });
                if (include.length && $scope.searchFormModel.query) {
                    $state.go('home.searchAll', {
                        'term': $scope.searchFormModel.query,
                        'type': $scope.searchFormModel.searchIn,
                        'where': include.join(',')
                    });
                }
            };
        }
    ]);