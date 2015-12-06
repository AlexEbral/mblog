'use strict';

angular.module('mblog', ['ngRoute', 'mblog.controllers', 'mblog.filters','mblog.directives', 'summernote', 'ngSanitize'])
    .config(['$routeProvider', '$locationProvider','$httpProvider', function($routeProvider, $locationProvider, $httpProvider) {
        $httpProvider.defaults.cache = false;
        if (!$httpProvider.defaults.headers.get) {
          $httpProvider.defaults.headers.get = {};
        }
        // disable IE ajax request caching
        $httpProvider.defaults.headers.get['If-Modified-Since'] = '0';

        $routeProvider.when('/', {templateUrl: '/static/js/app/partials/list-posts.html',
            controller: 'ListPostsCtrl'});
        $routeProvider.when('/new_post', {templateUrl: '/static/js/app/partials/post-editor.html',
            controller: 'PostEditorCtrl'});
        $routeProvider.when('/p/:post_id', {templateUrl: '/static/js/app/partials/post.html',
            controller: 'PostCtrl'});
        $routeProvider.when('/edit_post/:post_id', {templateUrl: '/static/js/app/partials/post-editor.html',
            controller: 'PostEditorCtrl'});
        $routeProvider.otherwise({redirectTo: '/'});
    }])
    .run(function($rootScope) {
       $rootScope.isAdmin = CURRENT_USER == 'admin';
       $rootScope.currentUser = CURRENT_USER;
    });