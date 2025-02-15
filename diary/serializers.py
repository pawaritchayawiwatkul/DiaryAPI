from rest_framework import serializers
from .models import Post, Comment, Picture

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at']

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['image', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    pictures = PictureSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['uuid','created_at', 'comments', 'pictures']

    def get_comments(self, obj):
        first_comment = obj.comments.first()
        return CommentSerializer(first_comment).data if first_comment else None
