from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    # me.followers.all() -> 나를 팔로우하는 모든 사용자에 접근
    # me.followings.all() -> 내가 팔로우하는 모든 사용자에 접근 