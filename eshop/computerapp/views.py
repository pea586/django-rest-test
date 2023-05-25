from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from computerapp.models import Product
from computerapp.serializers import ProductListSerializer



class ProductListView(generics.ListAPIView):
    """产品列表"""
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny, )
    filter_backends = (OrderingFilter, SearchFilter) # 默认的筛选字段，含全部字段。如需个性化筛选，请看下一行；
    # 后面的SearchFilter是搜索功能。配合下面一行的search_filter字段，实现搜索。
    ordering_fields = ('category', 'manufacturer', 'created', 'sold', ) # 排序字段，实现筛选目的
    search_fields = ('description', 'category', )
    ordering = ('id', )
    pagination_class = LimitOffsetPagination # 实现分页功能的调整
