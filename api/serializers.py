from rest_framework import serializers
from application.models import Product


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField(source='brand.name')

    class Meta:
        model = Product
        fields = ('name', 'price', 'brand')
