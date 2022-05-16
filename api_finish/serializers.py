from rest_framework import serializers
from matchat.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('state', 'key')