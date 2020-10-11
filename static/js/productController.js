app.controller("productCtrl", function($scope, $http, $window, $rootScope) {

    $rootScope.$on("productsRequestFunction", function(){
        $scope.productsRequestFunction();
    });

    /* GET PRODUCTS */
    $scope.productsRequestFunction = function(parameters = null){
        $scope.basicUrl = 'http://localhost:8000/api/product-list/?active=true';

        if($scope.isFilterProductActive && $scope.filterParameters != ""){
            $scope.basicUrl += $scope.filterParameters;
        }

        if (parameters !== null && parameters !== ''){
            $scope.basicUrl += parameters;
        }

        $scope.products_request = $http({
            method: 'GET',
            url: $scope.basicUrl
        }).then(function successCallback(response) {
            // this callback will be called asynchronously
            // when the response is available
            var products = response;
            $scope.products = products.data;

            /* PAGINATION PRODUCTS */
            $scope.paginationProductsFunction();

        }, function errorCallback(response) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });
    }

    $scope.productsRequestFunction();

    /* PRODUCTS SORT NAME */
    $scope.nameSortTypeProduct = "desc";
    $scope.productNameSort = function () {
        if($scope.nameSortTypeProduct == "desc"){
            $scope.nameSortTypeProduct = "asc";
        } else {
            $scope.nameSortTypeProduct = "desc";
        }
        $scope.productsRequestFunction("&name_sort=" + $scope.nameSortTypeProduct);
    }

    /* PRODUCTS SORT PRICE */
    $scope.priceSortTypeProduct = "desc";
    $scope.productPriceSort = function () {
        if($scope.priceSortTypeProduct == "desc"){
            $scope.priceSortTypeProduct = "asc";
        } else {
            $scope.priceSortTypeProduct = "desc";
        }
        $scope.productsRequestFunction("&price_sort=" + $scope.priceSortTypeProduct);
    }

    /* ADD PRODUCT */
    $scope.addProduct = function () {
        var element = document.getElementById('responseFromApi');
        var product = {
            name : $scope.productName,
            producer: $scope.productProducer,
            discounted_price: $scope.productDiscountedPrice || null,
            price: $scope.productPrice,
            is_active: true,
        };

        $scope.productName = "";
        $scope.productProducer = "";
        $scope.productDiscountedPrice = "";
        $scope.productPrice = "";

        $http.post("http://localhost:8000/api/product-create/", product)
            .then(function(response) {
                //Success
                $scope.productsRequestFunction();
                element.innerHTML = response.data;
                $('#myModal').modal();
            }, function(error) {
                element.innerHTML = error.data;
                $('#myModal').modal();
            });
    }

    /* PAGINATION PRODUCT */
    $scope.paginationProductsFunction = function() {
        var products_data = $scope.products;
        $scope.totalItemsProducts = $scope.products.length;
        $scope.currentPageProducts = 1;
        $scope.itemsPerPageProducts = 3;

        $scope.$watch("currentPageProducts", function() {
            setPagingDataProducts($scope.currentPageProducts);
        });

        function setPagingDataProducts(page) {
            var pagedData = products_data.slice((page - 1) * $scope.itemsPerPageProducts,page * $scope.itemsPerPageProducts);
            $scope.pagedDataProducts = pagedData;
        }
    }

    /* DELETE PRODUCT */
    $scope.removeRowProduct = function (product) {
        if ($window.confirm("Do you want to delete: " + product.name)) {
            var element = document.getElementById('responseFromApi');
            $http.delete("http://localhost:8000/api/product-delete/" + product.id)
            .then(function(response) {
                $scope.productsRequestFunction();
                element.innerHTML = response.data;
                $('#myModal').modal();
            }, function(error) {
                element.innerHTML = error.data;
                $('#myModal').modal();
            });
        }
    }

    /* EDIT PRODUCT */
    $scope.productNameEdit = "";
    $scope.productProducerEdit = "";
    $scope.productDiscountedPriceEdit = 0;
    $scope.productPriceEdit = 0;
    $scope.productIdEdit = 0;
    $scope.isEditProduct = false;
    $scope.productActiveEdit = false;

    $scope.editProduct = function (product) {
        $scope.isEditProduct = true;
        $scope.productNameEdit = product.name;
        $scope.productIdEdit = product.id;
        $scope.productProducerEdit = product.producer + "";
        $scope.productDiscountedPriceEdit = product.discounted_price;
        $scope.productPriceEdit = product.price;
        $scope.productActiveEdit = product.is_active + "";
    }

    $scope.saveChangesProduct = function () {
        var element = document.getElementById('responseFromApi');
        var product = {
            id: $scope.productIdEdit,
            name : $scope.productNameEdit,
            producer: $scope.productProducerEdit,
            discounted_price: $scope.productDiscountedPriceEdit,
            price: $scope.productPriceEdit,
            is_active: $scope.productActiveEdit,
        };

        $http.post("http://localhost:8000/api/product-update/" + $scope.productIdEdit + "/", product)
            .then(function(response) {
                //Success
                $scope.productsRequestFunction();
                element.innerHTML = response.data;

                $scope.productNameEdit = "";
                $scope.productProducerEdit = null;
                $scope.productDiscountedPriceEdit = 0;
                $scope.productPriceEdit = 0;
                $scope.productIdEdit = 0;
                $scope.isEditProduct = false;
                $scope.productActiveEdit = false;

                $('#myModal').modal();
            }, function(error) {
                element.innerHTML = error.data;
                $scope.isEditProduct = false;
                $('#myModal').modal();
            });
    }

    $scope.cancelChangesProduct = function () {
        $scope.productNameEdit = "";
        $scope.productProducerEdit = "";
        $scope.productDiscountedPriceEdit = 0;
        $scope.productPriceEdit = 0;
        $scope.productIdEdit = 0;
        $scope.isEditProduct = false;
    }

    /* PRODUCT FILTERS */
    $scope.productNameFilter = "";
    $scope.productProducerFilter = "";
    $scope.productDiscountedPriceFilter = null;
    $scope.productPriceFromFilter = null;
    $scope.productPriceToFilter = null;
    $scope.isFilterProductActive = false;
    $scope.filterParameters = "";

    $scope.searchProduct = function () {
        $scope.filterParameters = "";
        $scope.productNameFilter = $scope.productNameFilter;
        $scope.productProducerFilter = $scope.productProducerFilter;
        $scope.productDiscountedPriceFilter = $scope.productDiscountedPriceFilter;
        $scope.productPriceFromFilter = $scope.productPriceFromFilter;
        $scope.productPriceToFilter = $scope.productPriceToFilter;
        $scope.isFilterProductActive = true;

        if($scope.productNameFilter != null && $scope.productNameFilter != ""){
            $scope.filterParameters += ("&name=" + $scope.productNameFilter);
        }

        if($scope.productProducerFilter != null && $scope.productProducerFilter != ""){
            $scope.filterParameters += ("&producer=" + $scope.productProducerFilter);
        }

        if($scope.productDiscountedPriceFilter != null && $scope.productDiscountedPriceFilter != ""){
            $scope.filterParameters += ("&discounted=" + $scope.productDiscountedPriceFilter);
        }

        if($scope.productPriceFromFilter != null && $scope.productPriceFromFilter != ""){
            $scope.filterParameters += ("&from=" + $scope.productPriceFromFilter);
        }

        if($scope.productPriceToFilter != null && $scope.productPriceToFilter != ""){
            $scope.filterParameters += ("&to=" + $scope.productPriceToFilter);
        }

        $scope.productsRequestFunction($scope.filterParameters);

    }

    $scope.resetProduct = function () {
        $scope.productNameFilter = "";
        $scope.productProducerFilter = "";
        $scope.productDiscountedPriceFilter = null;
        $scope.productPriceFromFilter = null;
        $scope.productPriceToFilter = null;
        $scope.isFilterProductActive = false;
        $scope.filterParameters = "";
        $scope.productsRequestFunction();
    }


});