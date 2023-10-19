import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Article, Topic
from .serializers import ArticleListSerializer, ArticleSerializer, TopicSerializer


@api_view(['GET', 'POST'])
def article_list(request):
    # Article 테이블의 전체 데이터를 조회
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    
    # 
    elif request.method == 'POST':
        # 새로운 Article 인스턴스 생성 + Topic 인스턴스 생성 / Article-Topic 관계 생성
        # Topic 테이블의 데이터 입력을 저장하기(이미 테이블에 존재하는지 여부를 판단) 
        # request.data.get('topics')의 타입은 STR
        # request.data는 딕셔너리 타입 
        # -> key값을 통해 topic테이블에 입력하고자 하는 값에 접근
        topic_str = request.data.get('topics') # string type : "["test1", "test2", "test3"]"
        topic_list = json.loads(topic_str) # list type
        
        # 이미 있는 topic이면 topic테이블에 추가는 안 하지만
        # 관계는 설정
        topics = [] # 새롭게 추가되는 Topic 테이블의 인스턴스
        for topic in topic_list: # topic은 str type, 예를 들어 "test1"
            topic_data = { "name": topic }
            topic_serializer = TopicSerializer(data=topic_data) # serialize할 데이터를 인자로 전달
            # 이미 존재하는 topic이라면 값을 반환함
            exist_topic = Topic.objects.filter(name=topic).first()
            if exist_topic: # 이미 존재한다면
                topics.append(exist_topic) # <class 'articles.models.Topic'>
            else: # 새로운 토픽이라면
                # serialized된 값이 유효한 지 검사 
                if topic_serializer.is_valid(raise_exception=True):
                    # 유효하면 저장 - 테이블의 인스턴스를 저장하는 것과 같은 역할이지만 다른 메서드임
                    topic_serializer.save()
                    # 생성한 인스턴스를 리스트에 추가
                    topics.append(topic_serializer.instance)

        # 새로운 Article 인스턴스를 생성하기 위한 데이터 입력값을 serialize
        serializer = ArticleListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            article = serializer.save()
            # ★게시글 하나와 여러 개의 topic 사이의 관계(add)를 생성★
            article.topics.set(topics) # Article테이블에서 Topic테이블을 참조하여 관계 생성

            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, article_pk): 
    # 존재하지 않는 pk값을 전달하여 접근하려 한다면 에러가 발생
    # article = Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'GET':
        article.views += 1
        article.save()
        # ArticleSerializer를 맨 위에서 호출하여도 결과는 동일 : article을 참조하고 있기 때문에 
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        article.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        # 수정 시에 특정 필드만 입력받고 싶을 때 partial인자를 이용
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)