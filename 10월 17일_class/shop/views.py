from django.shortcuts import render, redirect
from .models import Product
import requests

# Create your views here.
def index(request):
    response = requests.get('https://fakestoreapi.com/products')
    products = response.json()

    # json 파일의 내용을 반복해서 저장
    for product in products:
        # 이미 저장된 상품이면 패스
        # filter()는 리스트를 반환
        if Product.objects.filter(title=product['title']).exists():
            continue
        title = product['title']
        description = product['description']
        price = int(product['price'] * 1300)
        image = product['image']
        Product.objects.create(
            title = title,
            description = description,
            price = price,
            image = image
        )
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'shop/index.html', context)


def addcart(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    user = request.user
    # 이미 장바구니에 있는 상품이라면, 장바구니에서 제거
    if product in user.cart.all():
        user.cart.remove(product)
    else:
        user.cart.add(product)
    
    return redirect('shop:index')
