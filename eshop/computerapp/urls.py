from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from computerapp import views


urlpatterns = [
    path('product_list/', views.ProductListView.as_view(), name='product_list'),

    path('product_list_by_category/', views.ProductListByCategoryView.as_view(),
         name='product_list_by_category'),

    path('product_list_by_category_manufacturer/', views.ProductListByCategoryManufacturerView.as_view(),
         name='product_list_by_category_manufacturer'),

    path('product_retrieve/<int:pk>/', views.ProductRetrieveView.as_view(), name='product_retrieve'),

    path('user_info/', views.UserInfoView.as_view(), name='user_info'),

    path('user_create/', views.UserCreateView.as_view(), name='user_create'),

    path('delivery_address_lc/', views.DeliveryAddressLCView.as_view(), name='delivery_address_lc'),

    path('delivery_address_rud/<int:pk>/', views.DeliveryAddressRUDView.as_view(),
         name='delivery_address_rud'),

]

urlpatterns = format_suffix_patterns(urlpatterns)