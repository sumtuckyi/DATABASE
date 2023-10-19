from rest_framework import serializers
from .models import Article, Comment, Topic


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


# 전체데이터 - 어떤 테이블의 어떤 필드의 데이터에 접근하고 유효성 검사를 실시해서 serialize할 것인지 정의
class ArticleListSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    
    class Meta:
        model = Article
        # 조회(GET) 시 접근할 속성 + 유효성 검사(POST, PUT) 시 확인할 속성
        fields = ('id', 'title', 'content', 'topics', )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        # 해당 필드에 대해 조회는 하지만, 유효성 검사 시에는 넘어가라
        read_only_fields = ('article', )


# 상세 데이터
class ArticleSerializer(serializers.ModelSerializer):
    # comment 내용 포함시키기
    # 1. CommentSerializer
    # comment_set = CommentSerializer(many=True, read_only=True) # 역참조 매니저 명으로 
    
    # 2. 각 필드를 재정의하기 
    # PrimaryKeyRelatedField : 참조하는 테이블의 PK
    # comment_id = serializers.PrimaryKeyRelatedField(source='comment_set', many=True, read_only=True)
    # comment_content = serializers.StringRelatedField(source='comment_set', many=True, read_only=True)
    
    # 3. SerializerMethodField  
    comments = serializers.SerializerMethodField()
    # 자동으로 get_comments 메서드를 호출
    def get_comments(self, obj):
        comments = obj.comment_set.all()
        return [{
            'id': comment.id,
            'content': comment.content,
        } for comment in comments]

    class Meta:
        model = Article
        fields = '__all__' # 역참조 시 사용되는 필드명도 추가가 되어있다. 


