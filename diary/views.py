from django.shortcuts import render
from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Prefetch

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'uuid'  # Ensures DRF uses UUID for lookups

    @action(detail=True, methods=['get'], url_path='comments', url_name='comments')
    def comments(self, request, uuid=None):
        post = Post.objects.prefetch_related(
            Prefetch('comments', queryset=Comment.objects.all(), to_attr='prefetched_comments')
        ).get(uuid=uuid)
        comments = post.prefetched_comments
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_uuid = self.request.data.get('post_uuid')
        post = Post.objects.get(uuid=post_uuid)
        serializer.save(post=post)
