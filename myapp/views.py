from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from .models import Producer, Product
from .serializers import ProducerSerializer, ProductSerializer


def index(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid credentials.')
            return redirect('index')
    return render(request, "index.html")


def home(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')
    return render(request, "home.html")


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def api_overview(request):
    api_urls = {
        'Producer List': '/producer-list/',
        'Producer Detail View': '/producer-detail/<str:pk>/',
        'Producer Create': '/producer-create/',
        'Producer Update': '/producer-update/<str:pk>/',
        'Producer Delete': '/producer-delete/<str:pk>/',
        'Product List': '/product-list/',
        'Product Detail View': '/product-detail/<str:pk>/',
        'Product Create': '/product-create/',
        'Product Update': '/product-update/<str:pk>/',
        'Product Delete': '/product-delete/<str:pk>/',
        'Product Specific Producer List': '/product-list/<str:producer>/',
    }
    return Response(api_urls)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def producer_list(request):
    producers = Producer.objects.all()

    name_sort = request.query_params.get('name_sort', None)
    if name_sort is not None and (name_sort == "asc" or name_sort == "desc"):
        if name_sort == "asc":
            producers = producers.order_by('name')
        if name_sort == "desc":
            producers = producers.order_by('-name')

    serializer = ProducerSerializer(producers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def producer_detail(request, pk):
    try:
        producer = Producer.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response('Resource not found', status=status.HTTP_404_NOT_FOUND)
    serializer = ProducerSerializer(producer, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def producer_create(request):
    if request.user.user_type == 'admin':
        serializer = ProducerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Producer successfully created", status=status.HTTP_201_CREATED)
        return Response("Create failed - data isnt correct", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    else:
        return Response('You dont have access or permission to create new Producer', status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def producer_update(request, pk):
    if request.user.user_type == 'admin':
        try:
            producer = Producer.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response('Update failed - resource not found', status=status.HTTP_404_NOT_FOUND)
        serializer = ProducerSerializer(instance=producer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Producer successfully updated", status=status.HTTP_200_OK)
        return Response("Update failed - data isnt correct", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    else:
        return Response('You dont have access or permission to update Producer data', status=status.HTTP_403_FORBIDDEN)


@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def producer_delete(request, pk):
    if request.user.user_type == 'admin':
        try:
            producer = Producer.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("Delete failed - resource not found", status=status.HTTP_404_NOT_FOUND)
        producer.delete()
        return Response("Producer successfully deleted", status=status.HTTP_202_ACCEPTED)
    else:
        return Response('You dont have access or permission to delete Producer', status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def product_list(request):
    products = Product.objects.all()

    is_active = request.query_params.get('active', None)
    if is_active is not None and (is_active == "false" or is_active == "true"):
        if is_active == "false":
            is_active = False
        elif is_active == "true":
            is_active = True
        products = products.filter(is_active=is_active)

    is_discounted_price = request.query_params.get('discounted', None)
    if is_discounted_price is not None and (is_discounted_price == "false" or is_discounted_price == "true"):
        if is_discounted_price == "false":
            is_discounted_price = True
        elif is_discounted_price == "true":
            is_discounted_price = False
        products = products.filter(discounted_price__isnull=is_discounted_price)

    price_from = request.query_params.get('from', None)
    price_to = request.query_params.get('to', None)
    try:
        if price_from is not None and (float(price_from) >= 0):
            products = products.filter(price__gte=price_from)
        if price_to is not None and (float(price_to) >= 0):
            products = products.filter(price__lte=price_to)
    except ValueError:
        pass
    except TypeError:
        pass

    name = request.query_params.get('name', None)
    if name is not None:
        products = products.filter(name=name)

    producer = request.query_params.get('producer', None)
    try:
        if producer is not None and (int(producer) >= 0):
            products = products.filter(producer=producer)
    except ValueError:
        pass
    except TypeError:
        pass

    name_sort = request.query_params.get('name_sort', None)
    if name_sort is not None and (name_sort == "asc" or name_sort == "desc"):
        if name_sort == "asc":
            products = products.order_by('name')
        if name_sort == "desc":
            products = products.order_by('-name')

    price_sort = request.query_params.get('price_sort', None)
    if price_sort is not None and (price_sort == "asc" or price_sort == "desc"):
        if price_sort == "asc":
            products = products.order_by('price')
        if price_sort == "desc":
            products = products.order_by('-price')

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def product_detail(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response('Resource not found', status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def product_create(request):
    if request.user.user_type == 'admin':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Product successfully created", status=status.HTTP_201_CREATED)
        return Response("Create failed - data isnt correct", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    else:
        return Response('You dont have access or permission to create Product', status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def product_update(request, pk):
    if request.user.user_type == 'admin':
        try:
            product = Product.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("Update failed - resource not found", status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Product successfully updated", status=status.HTTP_200_OK)
        return Response("Update failed - data isnt correct", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    else:
        return Response('You dont have access or permission to update Product', status=status.HTTP_403_FORBIDDEN)


@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def product_delete(request, pk):
    if request.user.user_type == 'admin':
        try:
            product = Product.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response("Delete failed - resource not found", status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response("Product successfully deleted", status=status.HTTP_202_ACCEPTED)
    else:
        return Response('You dont have access or permission to delete Product', status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def product_producer_list(request, producer):
    try:
        producer = Producer.objects.get(id=producer)
    except ObjectDoesNotExist:
        return Response('Resource not found', status=status.HTTP_404_NOT_FOUND)
    products = producer.product_set.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
