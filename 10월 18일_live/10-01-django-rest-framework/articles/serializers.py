from rest_framework import serializers
from .models import Article


# 전체 쿼리셋을 serialization
class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields= ('id', 'title', 'content')


# 단일 쿼리셋을 serialization - detail
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'