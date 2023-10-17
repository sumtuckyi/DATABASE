from django.urls import path, include
from . import views

app_name = "shop"
urlpatterns = [
    path('', views.index, name='index'),
    path('cart/<int:product_pk>/', views.addcart, name='addcart'),
]
