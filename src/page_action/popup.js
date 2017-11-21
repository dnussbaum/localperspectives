var payload = chrome.extension.getBackgroundPage().payload;

var app = angular.module("mainpopup", []);

app.controller("popupCtrl", function($scope, $http) {

    $scope.the_url = "";
    $scope.payload = {};

    chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
      $scope.$apply(function(){
        $scope.the_url = tabs[0].url;

        // JSON Request to get articles and other data
        $http({
          url: "http://127.0.0.1:5000/locations?url=" + encodeURIComponent($scope.the_url),
          method: "GET"
        }).then(function(response) {
          $scope.payload = response.data;

          for(var i=0; i < $scope.payload.locations.length; i++) {
            $http({
              url: "http://127.0.0.1:5000/?url=" + encodeURIComponent($scope.the_url) + "&location=" + encodeURIComponent($scope.payload.locations[i]),
              method: "GET"
            }).then(function(response) {
              $scope.payload.related_articles = $scope.payload.related_articles.concat(response.data.related_articles);
            });
          }

        });
      });
    });

    // Formats the date as needed
    $scope.format_date = function(date) {
      var d = new Date(date);
      return d.toLocaleDateString("en-US");
    };
});
