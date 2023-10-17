from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    # profile/을 넣는 이유 -> <username>만 있으면 위의 URL을 제외한 모든 URL입력에 대해 아래 패스로 연결되는 문제가 발생
    path('profile/<str:username>/', views.profile, name='profile'),
    path('<int:user_pk>/follow/', views.follow , name='follow'),
]
