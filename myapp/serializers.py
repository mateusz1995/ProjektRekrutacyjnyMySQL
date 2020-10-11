from rest_framework import serializers
from .models import Producer, Product


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        # Required fields
        fields = ('id', 'name',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # Required fields
        fields = ('id', 'name', 'producer', 'discounted_price', 'price', 'is_active',)

