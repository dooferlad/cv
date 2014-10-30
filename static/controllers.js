'use strict';

/* Controllers */

var cvControllers = angular.module('cvControllers', []);

cvControllers.controller('CVCtrl', ['$scope', '$http', '$routeParams',
    function($scope, $http, $routeParams) {

        $http.get('/API/career').success(function (data) {
            $scope.career = data;
        });
        $http.get('/API/education').success(function (data) {
            $scope.education = data;
        });
        $http.get('/API/jobs').success(function (data) {
            $scope.job_index = 0;
            data.some(function (job, index) {
                if (job.id === $routeParams.id) {
                    $scope.job_index = index;
                    return true;
                }
                return false;
            });

            $scope.job_spec = data[$scope.job_index];
            $scope.skills = [];
            $scope.missing_skills = [];

            $http.get('/API/skills').success(function (data) {
                $scope.job_spec.spec.every(function (desired_skill) {
                    desired_skill = desired_skill.trim();
                    if (desired_skill[0] === "!") {
                        return true;
                    }

                    var found = data.some(function (skill) {
                        if (skill.names.indexOf(desired_skill) >= 0) {
                            $scope.skills.push(skill);
                            return true;
                        }

                        return false;
                    });

                    if (!found) {
                        $scope.missing_skills.push(desired_skill);
                    }

                    return true;
                });
            });
        });
    }]);