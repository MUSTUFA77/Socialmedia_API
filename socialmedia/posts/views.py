from django.shortcuts import get_object_or_404
from .models import Post,PostComment,PostLike
from .serializers import PostSerializer,CommentSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

# Using API Views

class PostListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user_posts = Post.objects.filter(user=request.user)
        serializer = PostSerializer(user_posts, many=True)
        return Response({
            "success": True,
            "posts": serializer.data
        })
    
    def post(self,request):
        serializer = PostSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response({
                "success": True,
                "message": "Post created successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "success":True,
                "message":"Post updated successfully",
                "data":serializer.data
                })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.user == request.user:
            post.delete()
            return Response({
                "success": True,
                "message": "Post deleted successfully"
            },status=status.HTTP_204_NO_CONTENT)
        return Response({
            "success": False,
            "message": "You are not authorized to delete this post"}
            ,status=status.HTTP_401_UNAUTHORIZED)

class PostLikeAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post,pk=pk)
        likes_count = PostLike.objects.filter(post=post).count()
        return Response({
            "success": True,
            "likes": likes_count
        })

    def post(self, request, pk):
        post = get_object_or_404(Post,pk=pk)
        post_like, created = PostLike.objects.get_or_create(user=request.user, post=post)
        if not created:
            post_like.delete()
            return Response({
                "success": False,
                "message": "Post unliked"
            })
        else:
            return Response({
                "success": True,
                "message": "Post liked"
            })
class PostCommentAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post,pk=pk)
        comments = PostComment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response({
            "success": True,
            "comments": serializer.data
        })

    def post(self, request, pk):
        post = get_object_or_404(Post,pk=pk)
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(post=post)
            return Response({
                "success": True,
                "message": "Comment added"
            })
        else:
            return Response(serializer.errors, status=400)
        
    def delete(self,request,pk):
        comment = get_object_or_404(PostComment, pk=pk)
        if comment.user == request.user:
            comment.delete()
            return Response({
                "success": True,
                "message": "Comment deleted successfully"
            },status=status.HTTP_204_NO_CONTENT)
        return Response({
            "success": False,
            "message": "You dont have permissions to delete this comment"
        }, status=status.HTTP_403_FORBIDDEN)
