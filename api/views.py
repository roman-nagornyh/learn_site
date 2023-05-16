from django.shortcuts import render
from rest_framework import viewsets, pagination
from application.models import Product
from .serializers import ProductSerializer
from rest_framework import authentication


class DefaultPaginator(pagination.PageNumberPagination):
    page_size = 10


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('brand')
    serializer_class = ProductSerializer
    pagination_class = DefaultPaginator