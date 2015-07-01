angular.module('rdr')
    .controller("feeds/ArticlePreview", [
        '$scope', '$state', '$sce', '$modalInstance', 'article', 'feedsService',
        function($scope, $state, $sce, $modalInstance, article, feedsService) {

            var readArticle = {
                article: article
            };

            $scope.isLoading = true;
            $scope.readArticle = readArticle;

            feedsService.getFullArticleText(article.id).promise.then(function(res) {
                if (res.fullText) {
                    var fullText = res.fullText;
                    fullText.text = $sce.trustAsHtml(fullText.text);
                    $scope.readArticle.fullText = fullText;

                    if (!article.isRead) {
                        feedsService.markArticleAsRead(article);
                        $scope.$emit('article:read', article, article.feed);
                    }

                    $scope.isLoading = false;
                }
            });

            $scope.onClose = function(e) {
                e.preventDefault();
                $modalInstance.dismiss('cancel');
            };

            $scope.onAddToFavorites = function(article, e) {
                e.preventDefault();
                if (!article.isInFavorites) {
                    feedsService.addArticleToFavorites(article);
                } else {
                    feedsService.removeArticleFromFavorites(article);
                }
            }
        }
    ]);