from django.db import models

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=100)


class Article(models.Model):
    topics = models.ManyToManyField(Topic, blank=True, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 조회수는 상세페이지에서만 조회 가능
    views = models.IntegerField(default=0)


class Comment(models.Model):
    # Article 테이블을 참조 
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.content