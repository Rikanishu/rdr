angular.module('dummy', []);

angular.module('rdr', [
        'dummy',
        'ui.router',
        'ui.bootstrap',
        'lr.upload',
        'cfp.hotkeys',
        'ngDraggable',
        'nvd3ChartDirectives'
    ]).config(function($stateProvider, $urlRouterProvider) {

        $stateProvider
            .state("index", {
                url: "/",
                controller: "IndexCtrl"
            })
            .state("settings", {
                url: "/profile/settings",
                templateUrl: "static/js/partials/profile/settings.html",
                controller: "profile.SettingsCtrl"
            })
            .state("import-export", {
                url: "/profile/import-export",
                templateUrl: "static/js/partials/profile/import-export.html",
                controller: "profile.ImportExportCtrl"
            })
            .state("signup", {
                url: "/signup",
                templateUrl: "static/js/partials/profile/signup.html",
                controller: "users.SignUpCtrl",
                options: {
                    allowAnon: true
                }
            })
            .state("signin", {
                url: "/signin",
                templateUrl: "static/js/partials/profile/signin.html",
                controller: "users.SignInCtrl",
                options: {
                    allowAnon: true
                }
            })
            .state("signout", {
                url: "/signout",
                templateUrl: "static/js/partials/profile/quit.html",
                controller: "users.SignOutCtrl",
                options: {
                    allowAnon: false
                }
            })
            .state("home", {
                url: "/feeds",
                templateUrl: "static/js/partials/index.html",
                controller: "HomeCtrl"
            })
                .state("home.showFeed", {
                    url: "/list/:feedId",
                    templateUrl: "static/js/partials/feeds/list.html",
                    controller: "feeds.ShowFeedCtrl"
                })
                .state("home.unreadNews", {
                    url: "/unread",
                    templateUrl: "static/js/partials/feeds/list.html",
                    controller: "feeds.ShowUnreadNewsCtrl"
                })
                .state("home.addFeed", {
                    url: "/add",
                    templateUrl: "static/js/partials/feeds/add.html",
                    controller: "feeds.AddFeedCtrl"
                })
                .state("home.favorites", {
                    url: "/fav",
                    templateUrl: "static/js/partials/feeds/list.html",
                    controller: "feeds.ShowFavoritesCtrl"
                })
                .state("home.manageSubscribes", {
                    url: "/manage",
                    templateUrl: "static/js/partials/feeds/manage.html",
                    controller: "feeds/ManageCtrl"
                })
                .state("home.stats", {
                    url: "/stats",
                    templateUrl: "static/js/partials/feeds/stats.html",
                    controller: "feeds.StatsCtrl"
                })
                .state("home.searchFeed", {
                    url: "/search/:feed/:term/:type/:where",
                    templateUrl: "static/js/partials/feeds/search.html",
                    controller: "feeds.SearchCtrl"
                })
                .state("home.searchAll", {
                    url: "/search/:term/:type/:where",
                    templateUrl: "static/js/partials/feeds/search.html",
                    controller: "feeds.SearchCtrl"
                })
                .state("home.offlineQueue", {
                    url: "/offline-queue",
                    templateUrl: "static/js/partials/feeds/offline-queue.html",
                    controller: "feeds.OfflineQueueCtrl"
                })
            .state("tour", {
                url: "/tour",
                templateUrl: "static/js/partials/tour.html",
                controller: "TourCtrl",
                options: {
                    allowAnon: true
                }
            });

        $urlRouterProvider.otherwise('/');

    }
);

angular.module('rdr')
    .run(['$rootScope', '$state', '$http', 'userAuthService', 'initData',
        function($rootScope, $state, $http, userAuthService, initData) {
            $rootScope.$on('$stateChangeStart', function(event, nextState) {
                if (!userAuthService.isAuth() && (!nextState.options || !nextState.options.allowAnon)) {
                    event.preventDefault();
                    $state.go('tour');
                }
            });

            if (initData.csrfToken) {
                $http.defaults.headers.post['X-CSRFToken'] = initData.csrfToken;
            }

            userAuthService.runActivityChecking();

            console.log('===== Run application =====');
        }
    ]
);
