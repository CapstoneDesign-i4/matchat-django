from rest_framework import serializers
from matchat.models import *

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['key', 'kiosk_result', 'kiosk_photo'] # 인증번호, kiosk 사진에 대한 yolo 결과 값, kiosk 사진 경로 (챗봇용)