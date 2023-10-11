from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)

# 댓글 입력창을 추가 + 존재하는 댓글을 출력
def detail(request, pk): # variable routing으로 게시글의 pk를 사용, 인자로 넘겨주고 있음
    article = Article.objects.get(pk=pk) # article의 해당 인스턴스에 접근
    comment_form = CommentForm()
    # 해당 게시글의 모든 댓글을 조회(역참조)
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


@login_required
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('articles:index')


@login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid:
            form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/update.html', context)


# 사용자는 댓글 작성 시에 POST요청만 보내게 됨
def comments_create(request, pk):
    # 게시글 조회 : 댓글 생성시 외래키의 값이 필수이기 때문
    article = Article.objects.get(pk=pk)
    # 사용자로부터 입력받은 데이터(content)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid(): # 유효성 검사
        # comment_form을 저장하기 전에 누락된 외래키 값을 입력해주어야 한다. 
        # content값을 가진 인스턴스를 반환, db에 반영하지는 않음 
        comment = comment_form.save(commit=False)
        # 외래키 값을 입력
        comment.article = article
        # 필수값을 입력하고나서야 저장가능
        comment_form.save()
        return redirect('articles:detail', article.pk) # 디테일 페이지로 리다이렉트
    context = {
        'article': article,
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)

def comments_delete(request, article_pk, comment_pk):
    # 삭제할 댓글 조회
    comment = Comment.objects.get(pk=comment_pk)
    # article_pk = comment.article.pk
    comment.delete()
    return redirect('articles:detail', article_pk)