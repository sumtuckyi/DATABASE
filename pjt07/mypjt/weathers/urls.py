from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('save-data/', views.save_data),
    path('list-data/', views.list_data),
    path('hot-weathers/', views.hot_weathers),
]
