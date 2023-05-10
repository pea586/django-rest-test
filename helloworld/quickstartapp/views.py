from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User

from rest_framework import viewsets

from quickstartapp.serializers import UserSerializer





class UserViewSet(viewsets.ModelViewSet):
    """查看、编辑右后数据的API接口"""
    queryset = User.objects.all()
    serializer_class = UserSerializer