from rest_framework.response import Response
from rest_framework.views import APIView

from matchat.models import Product
from .serializers import ProductSerializer

class pay_check(APIView):
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)

        # 유효성 검사
        if serializer.is_valid():
            key = serializer.validated_data['key']  # key에 값 저장
            product = Product.objects.get(key=key)  # 해당 key를 가진 상품 호출

            # product state가 2이면 1 반환, 아니면 0 반환
            if int(product.state) == 2:
                data = {'status': '1'}
                return Response(data)
            else:
                data = {'status': '0'}
                return Response(data)


