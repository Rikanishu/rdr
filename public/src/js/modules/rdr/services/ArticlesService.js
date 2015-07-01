angular.module('rdr')
    .factory('articlesService', [
        '$q', '$http', '$modal',
        function($q, $http, $modal) {

            var Service = {};
            var fullTextModal;

            Service.getFullArticleText = function(article) {
                var def = $q.defer();
                $http.get('/articles/full-text', {'id': article.id}).success(function(data) {
                    def.resolve(data);
                }).error(function() {
                        def.reject();
                    });
                return def.promise;
            };

            Service.getArticleInfo = function(articleId, options) {
                var def = $q.defer();
                var reqParams = {};
                if (options.fullText) {
                    reqParams['full-text'] = 1;
                }
                $http.get('/feeds/articles/' + articleId + '/info', {params: reqParams}).success(function(data) {
                    def.resolve(data);
                }).error(function() {
                    def.reject();
                });
                return def.promise;
            };

            Service.openFullText = function(article) {
                if (angular.isObject(article)) {
                    openModal(article)
                } else {
                    Service.getArticleInfo(article).then(function(data) {
                        var article = data.article;
                        openModal(article);
                    });
                }

                function openModal(article) {
                    fullTextModal = $modal.open({
                        templateUrl: 'static/js/partials/feeds/preview.html',
                        controller: 'feeds/ArticlePreview',
                        size: 'lg',
                        resolve: {
                            article: function () {
                                return article;
                            }
                        }
                    });
                    fullTextModal.result.finally(function() {
                        fullTextModal = null;
                    });
                }

            };

            Service.isFullTextOpened = function() {
                return !!fullTextModal;
            };

            Service.closeFullText = function() {
                if (fullTextModal) {
                    fullTextModal.dismiss('cancel');
                    fullTextModal = null;
                }
            };

            return Service;
        }
    ]);
