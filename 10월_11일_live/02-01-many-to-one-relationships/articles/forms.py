from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

# 댓글 입력 폼 만들기
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )