from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework import permissions

from computerapp.models import Product
from computerapp.serializers import ProductListSerializer



class ProductListView(generics.ListAPIView):
    """产品列表"""
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny, )
    # filter_backends = (OrderingFilter, )
    # ordering_fields = ('category', 'manufacturer', 'created', 'sold', 'stock', )
    # ordering = ('id', )
