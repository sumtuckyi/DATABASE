# settings 모듈 가져오기
from django.conf import settings
from django.db import models

# from django.contrib.auth import get_user_model 
# from accounts.models import User

# Create your models here.
class Article(models.Model):
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # 외래키 추가
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
