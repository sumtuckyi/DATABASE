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


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
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
            article = form.save(commit=False)
            article.user = request.user
            form.save()
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
    if request.user == article.user:
        article.delete()
    return redirect('articles:index')


@login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid:
                form.save()
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/update.html', context)


@login_required
def comments_create(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment_form.save()
        return redirect('articles:detail', article.pk)
    context = {
        'article': article,
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)


@login_required
def comments_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('articles:detail', article_pk)


def likes(request, article_pk):
    # 별도의 페이지가 필요하지 않다. 게시글이 출력되는 페이지에 좋아요 버튼만 추가할 것이기 때문
    # 어떤 게시글에 좋아요를 누른 것인지 식별해야함
    article = Article.objects.get(pk=article_pk)
    
    # 좋아요를 추가할 것인지, 이미 누른 좋아요를 취소할 것인지 구분
    # ★현재 좋아요를 누른 유저가 해당 게시글에 좋아요를 누른 유저 목록에 있는지 확인★
    if request.user in article.like_users.all():
        # 좋아요 취소(2가지 방법)
        # 유저에서 역참조하여 좋아요 지우기
        # request.user.like_articles.remove(article)
        # 해당 게시글에서 특정 유저의 좋아요 지우기
        article.like_users.remove(request.user)
    else:
        # 추가(2가지 방법)
        # request.user.like_articles.add(article)
        article.like_users.add(request.user)
    return redirect('articles:index')