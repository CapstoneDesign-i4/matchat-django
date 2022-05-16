from rest_framework.response import Response
from rest_framework.views import APIView

from matchat.models import Product
from .serializers import ProductSerializer
from rest_framework import viewsets
from django.shortcuts import render

# Create your views here.

class ProductList(APIView):
    # 모든 데이터 가져오기 (API Test용)
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class Result(APIView):
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)

        # 유효성 검사
        if serializer.is_valid():
            key = serializer.validated_data['key']  # key에 값 저장
            product = Product.objects.get(key=key)  # 해당 key를 가진 상품 호출

            product.state = '3'
            product.save()

            data = {'key': product.key}
            return Response(data)