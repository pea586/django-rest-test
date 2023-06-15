from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from computerapp.models import Product, UserProfile, DeliveryAddress, Order

from computerapp.serializers import ProductListSerializer, ProductRetrieveSerializer, UserInfoSerializer, \
    UserSerializer, DeliveryAddressSerializer, OrderListSerializer, OrderCreateSerializer, OrderRUDSerializer




import datetime

import logging

LOG_FILENAME = 'shop.log'

# logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG) # 与下面一行确定logging记录的最低级别
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)



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


class ProductListByCategoryView(generics.ListAPIView):
    """产品按类别列表"""
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter, )
    search_fields = ('description', )
    ordering_fields = ('category', 'manufacturer', 'created', 'sold', 'stock', 'price', )
    ordering = ('id', )

    def get_queryset(self):
        category = self.request.query_params.get('category', None)

        if category is not None:
            queryset = Product.objects.filter(category = category)
        else:
            queryset = Product.objects.all()
        return queryset


class ProductListByCategoryManufacturerView(generics.ListAPIView):
    """产品按类别按品牌列表"""
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter, )
    search_fields = ('description', )
    ordering_fields = ('category', 'manufacturer', 'created', 'sold', 'stock', 'price', )
    ordering = ('id', )

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        manufacturer = self.request.query_params.get('manufacturer', None)

        if category is not None:
            queryset = Product.objects.filter(category = category, manufacturer=manufacturer)
        else:
            queryset = Product.objects.all()
        return queryset


class ProductRetrieveView(generics.RetrieveAPIView): # 可以改成generics.ListAPIView，效果为全部显示出来
    """详情页面"""
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer
    permission_classes = (permissions.AllowAny, )


class UserInfoView(APIView):
    """用户基本信息"""
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        user = self.request.user # 把当前用户的信息赋值给user，确保最后返回的data是当前用户的。避免查看别人的信息
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)


class UserCreateView(generics.CreateAPIView):
    """用户创建（用户注册）"""
    serializer_class = UserSerializer


class DeliveryAddressLCView(generics.ListCreateAPIView):
    """收货地址LC"""
    serializer_class = DeliveryAddressSerializer # 列表和详情共用一个序列器，因地址功能简单，仅电话、地址等信息
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        """确保当前用户只能查询当前用户的地址信息"""
        user = self.request.user # 获取当前用户
        queryset = DeliveryAddress.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        """实现当前用户创建的地址只能储存在当前用户名下"""
        user = self.request.user
        s = serializer.save(user=user)
        profile = user.profile_of # profile_of和models.py里的UserProfile的related_name相关联
        profile.delivery_address = s # profile的delivery_address字段
        profile.save()


class DeliveryAddressRUDView(generics.RetrieveUpdateDestroyAPIView):
    """收货地址RUD"""
    serializer_class = DeliveryAddressSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        user = self.request.user

        try: # 由于一个用户可能对应多个收货地址，需要id和user完全匹配，才会返回obj
            obj = DeliveryAddress.objects.get(id=self.kwargs['pk'], user=user) # pk是urls里的正则表达式内的pk
        except Exception as e:
            raise NotFound('not found')
        return obj


class CartListView(generics.ListAPIView):
    """Cart List"""
    serializer_class = OrderListSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(user=user, status='0')
        return queryset


class OrderListView(generics.ListAPIView):
    """Order list"""
    serializer_class = OrderListSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(user=user, status__in=['1', '2', '3', '4'])
        return queryset


class OrderCreateView(generics.CreateAPIView):
    """Order create"""
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data.get('product')
        serializer.save(user=user, price=product.price,
                        address=self.request.user.profile_of.delivery_address)

        logging.info('user %d cart changed, product %d related. Time is %d.', user.id, product.id,
                     str(datetime.datetime.now()))


class OrderRUDView(generics.RetrieveUpdateDestroyAPIView):
    """Order RUD"""
    serializer_class = OrderRUDSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        user = self.request.user
        obj = Order.objects.get(user = user, id=self.kwargs['pk'])
        return obj

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(user=user, status = '1') # status=1表示状态由购物车转到未付款订单，防止被修改为已支付订单
