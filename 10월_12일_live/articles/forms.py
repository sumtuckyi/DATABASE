from django import forms

from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        # fields = ('title', 'content', )
        # user 필드를 폼에서 보이지 않게 하므로 이 필드가 입력되지 않게됨 
        # -> 현재 로그인 된 유저의 정보가 해당 필드에 입력되어야 함 
        exclude = ('user', )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
    
