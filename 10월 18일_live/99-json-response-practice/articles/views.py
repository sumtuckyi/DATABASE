from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ArticleSerializer
from .models import Article

# Create your views here.


# @api_view(['GET'])
@api_view()
def article_json(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data) # 기존의 render()를 이용한 응답이 아님
