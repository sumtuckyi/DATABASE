from django.db import models
from django.conf import settings


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    # 이미지 url을 저장
    image = models.URLField()
    # 장바구니(중개 테이블 자동 생성)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='cart', blank=True)
    