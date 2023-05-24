from rest_framework import serializers


from computerapp.models import Product

class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'model', 'image', 'price', 'sold', 'category', 'manufacturer', ]