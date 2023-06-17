from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    commented_by = serializers.ReadOnlyField(source ='user.username')
    class Meta:
        model = Comment
        fields = ['comment','post','commented_by','comment_date']