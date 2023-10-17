from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect('articles:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def delete(request):
    request.user.delete()
    return redirect('articles:index')


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def change_password(request, user_pk):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)


@login_required
def profile(request, username):
    # 사용자의 detail page를 렌더링하기 
    # User를 조회(로그인 한 유저와 다를 수 있음)
    person = get_user_model().objects.get(username=username) # 커스텀 User모델은 직접 참조하지 않음
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def follow(request, user_pk):
    # follow할 대상을 조회
    you = User.objects.get(pk=user_pk)
    me = request.user # 'test01'

    if me != you: # 자기 자신을 팔로우 할 수는 없음
        # follow를 하는 것인지, 기존의 것을 취소하는 것인지 판단
        # exists() 사용해보기 - me가 you의 followers에 포함되어있는지
        if you.followers.filter(username=me).exists(): 
        # if me in you.followers.all():
            you.followers.remove(me)
            # me.follwings.remove(you)
        else:
            you.followers.add(me)
            # me.followings.add(you)
        return redirect('articles:index')
  

