'use strict';

angular.module('mblog.controllers', ['restangular'])
.config(['RestangularProvider', '$locationProvider', function(RestangularProvider, $locationProvider) {
        RestangularProvider.setBaseUrl('/api');
        RestangularProvider.setDefaultHttpFields({ cache: false });
		RestangularProvider.setResponseExtractor(function(response, operation) {
		      var newResponse;
		      if (operation === "getList") {
		        newResponse = response.data;
		        newResponse.metadata = {
		        		success: response.success,
		        		results: response.data ? response.data.length : 0,
		        		page: 1,
		        		totalPages: 1
		        	};
		      }
		      else {
		        newResponse = response;
		      }
		      return newResponse;
		    });
        RestangularProvider.addResponseInterceptor(function(resp) {
            if(resp.status && resp.status == 403) {
                window.location.href = '/login';
                return resp;
            }
            else {
                return resp;
            }
        });
		RestangularProvider.setErrorInterceptor(function(resp) {
	    	if(resp.status !== 200) {
                $.notify("Произошла неизвестная ошибка", {
                    placement: {
                        from: 'top',
                        align: 'center'
                    },
                    type: "danger"
                });
                console.log("Произошла неизвестная ошибка");
	    		return true;
	    	}
	    	return true;
	    });

        $locationProvider.html5Mode({enabled: true, requireBase: false}).hashPrefix('');
    }])
.controller('ListPostsCtrl', ['$scope', '$location', '$window', '$interval', 'Restangular',
        function($scope, $location, $window, $interval, Restangular) {
            $scope.postsLimit = 5;
            $scope.pageNum = 0;

            $scope.loadPosts = function(){
                Restangular.one('posts', $scope.pageNum * $scope.postsLimit).one('', $scope.postsLimit).get().then(function(resp){
                    $scope.isOlderPosts = resp.data.is_older_posts;
                    $scope.posts = _.sortBy(resp.data.posts, 'datetime').reverse();
                });
            }

            $scope.nextPage = function(){
                 $scope.pageNum += 1;
                 $scope.loadPosts();
            }

            $scope.prevPage = function(){
                 $scope.pageNum -= 1;
                 $scope.loadPosts();
            }

            $scope.loadPosts();
    }])
.controller('PostEditorCtrl', ['$scope', '$location', '$window', '$interval', 'Restangular', '$routeParams',
        function($scope, $location, $window, $interval, Restangular, $routeParams) {
            $scope.new_post = null;
            $scope.isNewPost = $routeParams.post_id == undefined;

            if(!$scope.isNewPost){
                Restangular.one('post', $routeParams.post_id).get().then(function(resp){
                    $scope.new_post = resp;
                    $scope.isAuthor = CURRENT_USER == $scope.new_post.author;
                });
            }

            $scope.createPost = function(){
                $scope.new_post.author = $scope.currentUser;
                Restangular.all('post').post($scope.new_post).then(function(resp){
                    $location.path('/');
                });
            }

            $scope.updatePost = function(){
                $scope.new_post.author = $scope.currentUser;
                $scope.new_post.id = $routeParams.post_id;
                delete $scope.new_post.comments;
                $scope.new_post.put().then(function(resp){
                    $location.path('/');
                });
            }

            $scope.deletePost = function(){
                $scope.new_post.author = $scope.currentUser;
                Restangular.one('post', $routeParams.post_id).remove().then(function(resp){
                    $location.path('/');
                });
            }

    }])
.controller('PostCtrl', ['$scope', '$location', '$window', '$interval', 'Restangular', '$routeParams', '$sce',
        function($scope, $location, $window, $interval, Restangular, $routeParams, $sce) {

            Restangular.one('post', $routeParams.post_id).get().then(function(resp){
                $scope.post = resp;
                $scope.isAuthor = CURRENT_USER == $scope.post.author;
                $scope.currentUser = CURRENT_USER;
                $scope.newComment = null;
                $scope.isEdit = false;
            });

            $scope.editPost = function(){
                $location.path('/edit_post/' + $routeParams.post_id);
            }

            $scope.editComment = function(comment){
                comment.isEdit = true;
            }

            $scope.updateComment = function(comment){
               comment = $scope.schedule = Restangular.restangularizeElement(null, comment, 'comment');
               delete comment.isEdit;
               comment.put().then(function(resp){
                    comment = resp.data;
                });
            }

            $scope.trustAsHtml = function(html) {
              return $sce.trustAsHtml(html);
            }

            $scope.deleteComment = function(comment){
                var index = $scope.post.comments.indexOf(comment);
                if (index > -1) {
                    $scope.post.comments.splice(index, 1);
                }
                Restangular.one('comment', comment.id).remove();
                comment.isEdit = false;
            }

            $scope.sendComment = function(){
                $scope.newComment.author = CURRENT_USER;
                $scope.newComment.post_id = $routeParams.post_id;

                Restangular.all('comment').post($scope.newComment).then(function(resp){
                    $scope.post.comments.push(resp.data);
                    $scope.newComment = null;
                });
            }
    }]);