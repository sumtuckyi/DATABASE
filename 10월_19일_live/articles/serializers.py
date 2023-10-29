from rest_framework import serializers
from .models import Article, Comment


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content',)


class CommentSerializer(serializers.ModelSerializer):
    class ArticleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('title', )

    # override
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        # read_only_fields = ('article', ) # 조회 시에는 포함되지만, 유효성 검사 시에는 포함되지 않는 필드


class ArticleSerializer(serializers.ModelSerializer):
    # class CommentSerializer(serializers.ModelSerializer):
    #     class Meta:
    #         model = Comment
    #         fields = ('content', )

    # 기존에 있는 serializer 사용, 커스텀하여 만들어도 됨
    # many=True는 하나의 Article 인스턴스에 여러개의 Comment 인스턴스가 연결될 수 있음을 나타냄
    # read_only=True는 데이터를 입력받아 새로운 Article 인스턴스 생성 시에 해당 필드가 입력될 필요는 없지만, 조회 시에는 출력됨을 나타냄 
    comment_set = CommentSerializer(many=True, read_only=True)
    # 역참조하여 새로운 필드를 생성 - 해당 필드는 JSON 응답 반환 시에만 존재함? -> yes, read_only=True이기 때문
    # source='comment_set.count'에는 queryset 명령어가 그대로 들어감
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__' # 모든 필드에 대해서 유효성 검사를 진행



class Serializer(serializers.Serializer):
    pass
