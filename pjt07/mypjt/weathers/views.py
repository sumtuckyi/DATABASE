from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
import requests
from .serializers import WeatherSerializer
from .models import Weather

# Create your views here.
@api_view(['GET'])
def index(request):
    # api_key = settings.API_KEY
    api_key = '0332c0051f7ca78500b4da9363a3ca89'
    city = 'Seoul,KR'
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()
    
    return Response(response)

@api_view(['GET'])
def save_data(request):
    api_key = settings.API_KEY
    city = 'Seoul,KR'
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}'
    response = requests.get(url).json()
    # api 요청을 보내고 받아온 응답 데이터
    for li in response.get("list"):
        save_data = {
            'dt_txt': li.get('dt_txt'),
            'temp': li.get('main').get('temp'),
            'feels_like': li.get('main').get('feels_like')
        }
        # 저장하기 위해 데이터를 serialize
        serializer = WeatherSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    
    # 저장완료 메세지를 사용자에게 보여줌
    return JsonResponse({ 'message':'okay' })


# DB에 저장된 전체 데이터 조회
@api_view(['GET'])
def list_data(request):
    weathers = Weather.objects.all()
    serializer = WeatherSerializer(weathers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def hot_weathers(request):
    # 데이터베이스에서 데이터를 가져올 때 필터링 하기 - filter()사용하기
    weathers = Weather.objects.all()
    hot_weathers = []
    for weather in weathers:
        tmp = round(weather.temp - 273.15, 2)
        if tmp > 20:
            hot_weathers.append(weather)
    serializer = WeatherSerializer(hot_weathers, many = True) 
    return Response(serializer.data)
    # serialize할 때 필터링 하기 - serializer 파일 수정