from rest_framework import serializers
from .models import Post
from comments.serializers import CommentSerializer
from likes.serializers import LikeSerializer

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['user', 'title', 'content', 'tags', 'image', 'time', 'comments', 'likes']
