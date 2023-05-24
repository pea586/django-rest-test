from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from computerapp import views

urlpatterns = [
    path('product_list/', views.ProductListView.as_view(), name='product_list'),

]

urlpatterns = format_suffix_patterns(urlpatterns)