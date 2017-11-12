var payload = chrome.extension.getBackgroundPage().payload;

var app = angular.module("mainpopup", []);

app.controller("popupCtrl", function($scope, $http) {

    $scope.the_url = "";
    $scope.payload = {};

    chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
      $scope.$apply(function(){
        $scope.the_url = tabs[0].url;

        // JSON Request to get articles and other data
        $http.get("/js/json_output.json").then(function(response) {
          $scope.payload = response.data;
        });
      });
    });

    // Formats the date as needed
    $scope.format_date = function(date) {
      var d = new Date(date);
      return d.toLocaleDateString("en-US");
    };
});
