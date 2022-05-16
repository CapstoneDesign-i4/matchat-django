from django.db import models
from django.contrib.auth.models import User

def directory_path(instance, filename):
    return f'{instance.product.author}/{instance.product.name}/{filename}'

class Product(models.Model):
    name = models.CharField(max_length=100) # 상품명
    use_period = models.CharField(max_length=50) # 사용기간
    price = models.CharField(max_length=10) #가격
    content = models.TextField(null=True)
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    reservation = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservation', null=True, blank=True)
    state = models.CharField(max_length=1, default='0')
    key = models.IntegerField(null=True)  # 우리가 랜덤으로 부여
    place = models.CharField(max_length=10, default='이대역') # 지점
    kiosk_photo = models.CharField(max_length=2090, null=True, blank=True) #kiosk 사진의 url 저장
    kiosk_result = models.CharField(max_length=100, default='none')
    web_result = models.CharField(max_length=100, default='none')

    def __str__(self):
        return self.name

class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to=directory_path, blank=True, null=True)

class Credit_Info(models.Model):
    card_com= models.CharField(max_length=20)
    card_num1=models.CharField(max_length=20)
    card_num2=models.CharField(max_length=20)
    card_num3=models.CharField(max_length=20)
    card_num4=models.CharField(max_length=20)
    cvc_num=models.CharField(max_length=20)
    dead_year=models.CharField(max_length=20)
    dead_month=models.CharField(max_length=20)


