/**
 * Created by dooferlad on 31/05/14.
 */

var cvApp = angular.module('cvApp', [
  'ngRoute',
  'cvControllers',
  'ui.bootstrap'
]);

cvApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/', {
                templateUrl: '/static/home.html',
                controller: 'CVCtrl'
            }).
            when('/job/:id', {
                templateUrl: '/static/cv.html',
                controller: 'CVCtrl'
            }).
            otherwise({ redirectTo: '/' });
    }]);
