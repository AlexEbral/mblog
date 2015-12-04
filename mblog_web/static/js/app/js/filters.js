angular.module('mblog.filters',[])
.filter('trustAsHtml', function($sce){
    return function(html){
        return $sce.trustAsHtml(html);
    };
});