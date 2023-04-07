from rest_framework import serializers
from .models import Product
from .models import ProductImage


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'price', 'category', 'is_active')

# class ProductImageSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = ProductImage
#        fields = ('product', 'image', 'is_active')
