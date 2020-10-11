from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),

    # API URLS
    path('api/', views.api_overview, name='api_overview'),
    path('api/producer-list/', views.producer_list, name='producer_list'),
    path('api/producer-detail/<str:pk>/', views.producer_detail, name='producer_detail'),
    path('api/producer-create/', views.producer_create, name='producer_create'),
    path('api/producer-update/<str:pk>/', views.producer_update, name='producer_update'),
    path('api/producer-delete/<str:pk>/', views.producer_delete, name='producer_delete'),
    path('api/product-list/', views.product_list, name='product_list'),
    path('api/product-detail/<str:pk>/', views.product_detail, name='product_detail'),
    path('api/product-create/', views.product_create, name='product_create'),
    path('api/product-update/<str:pk>/', views.product_update, name='product_update'),
    path('api/product-delete/<str:pk>/', views.product_delete, name='product_delete'),
    path('api/product-list/<str:producer>/', views.product_producer_list, name='product_producer_list'),

]