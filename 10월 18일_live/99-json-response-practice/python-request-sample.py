import requests
from pprint import pprint

# 해당 서버가 켜져 있어야 응답을 받을 수 있음에 유의
response = requests.get('http://127.0.0.1:8000/api/v1/articles/')

# json을 python 타입으로 변환
result = response.json()

print(type(result)) # <class 'list'>
# pprint(result) 
pprint(type(result[0])) # <class 'dict'>
pprint(result[0].get('title'))
