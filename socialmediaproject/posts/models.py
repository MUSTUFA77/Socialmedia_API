from django.db import models
from django.contrib.auth.models import User
# from comments.models import Comment
# from likes.models import Like
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='uploaded-images/')
    tags = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    # comments = models.ManyToManyField(Comment,related_name='post_comments')
    # likes = models.ManyToManyField(Like,related_name='post_likes')

    def __str__(self):
        return self.title