from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Article
from .serializers import ArticleListSerializer, ArticleSerializer


# 게시글을 전체 조회 / 신규 게시글 작성
@api_view(['GET', 'POST']) # 함수 실행 전에 확인 
def article_list(request):
    if request.method == 'GET': # 전체 게시글 조회 기능 구현
        articles = Article.objects.all()
        # 데이터 타입을 변환
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data) # serializer.data로 JSON으로 변환됨 -> 반환

    # 게시글 작성 요청을 보냈을 때
    elif request.method == 'POST': # 게시글 작성 기능 구현
        # 이제는 form이 아닌 serializer로 데이터를 받아서 저장
        serializer = ArticleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def article_detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)

    if request.method == 'GET': # 단일 게시글 조회기능 구현(상세페이지)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'DELETE': # 삭제기능 구현
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT': # 수정기능 구현
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)