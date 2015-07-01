angular.module('rdr')
    .factory('feedsService', [
        '$q', '$http', 'l10n',
        function($q, $http, l10n) {

            var Service = {};

            Service.getArticles = function(feedId, options) {
                var def = $q.defer();
                var requestParams = {};
                if (options) {
                    if (options.page) {
                        requestParams.page = options.page;
                    }
                }
                $http.get('/feeds/' + feedId + '/articles/list', {params: requestParams})
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function() {
                        def.reject();
                    });

                return def.promise;
            };

            Service.getFullArticleText = function(articleId) {
                var requestDef = $q.defer();
                var cancelDef = $q.defer();
                $http.get('/feeds/articles/' + articleId + '/full-text', {
                    timeout: cancelDef.promise
                }).success(function(response) {
                        requestDef.resolve(response);
                })
                .error(function() {
                        requestDef.reject();
                });

                return {
                    promise: requestDef.promise,
                    cancel: cancelDef
                };
            };

            Service.markArticleAsRead = function(article) {
                var def = $q.defer();
                $http.post('/feeds/articles/mark-as-read', {articleId: article.id})
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function() {
                        def.reject();
                    });

                return def.promise;
            };

            Service.getAllUnreadNews = function(options) {
                var def = $q.defer();
                var requestParams = {};
                if (options) {
                    if (options.page) {
                        requestParams.page = options.page;
                    }
                }
                $http.get('/feeds/unread/articles/list', {params: requestParams})
                    .success(function(response) {
                        //todo: isDifferentSources
                        response.feed = {
                            title: l10n('Unread news'),
                            iconSrc: '/static/img/feeds/book-120x80.png'
                        };
                        def.resolve(response);
                    })
                    .error(function() {
                        def.reject();
                    });

                return def.promise;
            };

            Service.markFeedArticlesAsRead = function(feedId) {
                var def = $q.defer();
                $http.post('/feeds/mark-all-as-read', {feedId: feedId})
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function() {
                        def.reject();
                    });

                return def.promise;
            };

            Service.markAllUnreadAsRead = function(feedId) {
                var def = $q.defer();
                $http.post('/feeds/mark-all-unread-as-read')
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function() {
                        def.reject();
                    });

                return def.promise;
            };

            Service.getFeedDetail = function(feedId) {
                var def = $q.defer();
                $http.get('/feeds/' + feedId + '/info')
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function() {
                        def.reject();
                    });

                return def.promise;
            };

            Service.syncArticles = function(feedId) {
                var def = $q.defer();
                $http.get('/feeds/' + feedId + '/articles/sync')
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function() {
                        def.reject();
                    });

                return def.promise;
            };

            Service.getFavoriteArticles = function(options) {
                var def = $q.defer();
                var requestParams = {};
                if (options) {
                    if (options.page) {
                        requestParams.page = options.page;
                    }
                }
                $http.get('/feeds/favorites/articles/list', {params: requestParams})
                    .success(function(response) {
                        response.feed = {
                            title: l10n('Favorites'),
                            iconSrc: '/static/img/feeds/book-120x80.png'
                        };
                        def.resolve(response);
                    })
                    .error(function() {
                        def.reject();
                    });

                return def.promise;
            };

            Service.addArticleToFavorites = function(article) {
                var def = $q.defer();
                $http.post('/feeds/favorites/articles/add', {articleId: article.id})
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function() {
                        def.reject();
                    });

                article.isInFavorites = true;

                return def.promise;
            };

            Service.removeArticleFromFavorites = function(article) {
                var def = $q.defer();
                $http.post('/feeds/favorites/articles/remove', {articleId: article.id})
                    .success(function(response) {
                        def.resolve(response);
                    })
                    .error(function() {
                        def.reject();
                    });

                article.isInFavorites = false;

                return def.promise;
            };

            return Service;

        }
    ]);
