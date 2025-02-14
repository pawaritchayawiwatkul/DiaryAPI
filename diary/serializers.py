from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['uuid', 'image', 'created_at', 'comments']

    def get_comments(self, obj):
        first_comment = obj.comments.first()
        return CommentSerializer(first_comment).data if first_comment else None
