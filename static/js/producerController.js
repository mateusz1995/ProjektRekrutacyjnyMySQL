app.controller("producerCtrl", function($scope, $http, $window, $rootScope) {


    /* GET PRODUCERS */
    $scope.producersRequestFunction = function(parameters = null) {
        $scope.basicUrl = 'http://localhost:8000/api/producer-list/';
        if (parameters !== null && parameters !== ''){
            $scope.basicUrl += parameters;
        }
        $scope.producers_request = $http({
            method: 'GET',
            url: $scope.basicUrl
        }).then(function successCallback(response) {
            // this callback will be called asynchronously
            // when the response is available
            var producers = response;
            $rootScope.producers = producers.data;

            /* PAGINATION PRODUCERS */
            $scope.paginationProducersFunction();

        }, function errorCallback(response) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });
    }

    $scope.producersRequestFunction();

    /* PAGINATION PRODUCERS */
    $scope.paginationProducersFunction = function() {
        var producers_data = $scope.producers;
        $scope.totalItemsProducers = $scope.producers.length;
        $scope.currentPageProducers = 1;
        $scope.itemsPerPageProducers = 3;

        $scope.$watch("currentPageProducers", function() {
            setPagingDataProducers($scope.currentPageProducers);
        });

        function setPagingDataProducers(page) {
            var pagedData = producers_data.slice((page - 1) * $scope.itemsPerPageProducers, page * $scope.itemsPerPageProducers);
            $scope.pagedDataProducers = pagedData;
        }
    }

    /* PRODUCERS SORT NAME */
    $scope.nameSortTypeProducer = "desc";
    $scope.producersNameSort = function () {
        if($scope.nameSortTypeProducer == "desc"){
            $scope.nameSortTypeProducer = "asc";
        } else {
            $scope.nameSortTypeProducer = "desc";
        }
        $scope.producersRequestFunction("?name_sort=" + $scope.nameSortTypeProducer);
    }

    /* ADD PRODUCER */
    $scope.addProducer = function () {
        var element = document.getElementById('responseFromApi');
        var producer = {
            name : $scope.producerName,
        };
        $scope.producerName = "";
        $http.post("http://localhost:8000/api/producer-create/", producer)
            .then(function(response) {
                //Success
                $scope.producersRequestFunction();
                element.innerHTML = response.data;
                $('#myModal').modal();
            }, function(error) {
                element.innerHTML = error.data;
                $('#myModal').modal();
            });
    }

    /* DELETE PRODUCER */
    $scope.removeRowProducer = function (producer) {
        if ($window.confirm("Do you want to delete: " + producer.name)) {
            var element = document.getElementById('responseFromApi');
            $http.delete("http://localhost:8000/api/producer-delete/" + producer.id)
            .then(function(response) {
                $scope.producersRequestFunction();
                $rootScope.$emit("productsRequestFunction", {});
                element.innerHTML = response.data;
                $('#myModal').modal();
            }, function(error) {
                element.innerHTML = error.data;
                $('#myModal').modal();
            });
        }
    }

    /* EDIT PRODUCER */
    $scope.producerNameEdit = "";
    $scope.producerIdEdit = 0;
    $scope.isEditProducer = false;

    $scope.editProducer = function (producer) {
        $scope.isEditProducer = true;
        $scope.producerNameEdit = producer.name;
        $scope.producerIdEdit = producer.id;
    }

    $scope.saveChangesProducer = function () {
        var element = document.getElementById('responseFromApi');
        var producer = {
            id: $scope.producerIdEdit,
            name : $scope.producerNameEdit,
        };

        $http.post("http://localhost:8000/api/producer-update/" + $scope.producerIdEdit + "/", producer)
            .then(function(response) {
                //Success
                $scope.producersRequestFunction();
                $rootScope.$emit("productsRequestFunction", {});
                element.innerHTML = response.data;

                $scope.isEditProducer = false;
                $scope.producerNameEdit = ""
                $scope.producerIdEdit = 0

                $('#myModal').modal();
            }, function(error) {
                element.innerHTML = error.data;
                $('#myModal').modal();
            });
    }

    $scope.cancelChangesProducer = function () {
        $scope.isEditProducer = false;
        $scope.producerNameEdit = ""
        $scope.producerIdEdit = 0
    }

});