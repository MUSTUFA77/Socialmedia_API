from django.shortcuts import get_object_or_404
from .models import Post,PostComment,PostLike
from .serializers import PostSerializer,PostLikeSerializer,CommentSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

# class CreatePost(generics.CreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

# class RetrievePost(generics.RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class UpdatePost(generics.UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class= PostSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def put(self,request,pk):
#         post = Post.objects.get(id=pk)
#         serializer = PostSerializer(post, data = request.data ,partial = True)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response({
#                 "success":True,
#                 "message":"Updated the post"
#             })
#         else:
#             print(serializer.errors)
#             return Response({
#                 "success":False,
#                 "message":"Error updating the post"
#             })
        
# class DeletePost(generics.DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class= PostSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def destroy(self, request, *args, **kwargs):
#         try:
#             pk = kwargs.get("pk")
#             post = Post.objects.get(id = pk)
#             if post.user.id == request.user.id:
#                 self.perform_destroy(post)
#                 return Response({
#                     "success":True,
#                     "message":"post deleted"
#                 })
#             else:
#                 return Response({
#                     "success":False,
#                     "message":"You are not authorized to delete this post"
#                 })
#         except ObjectDoesNotExist:
#             return Response({
#                 "success":False,
#                 "message":"Post does not Exist"
#             })
        
# class RetrieveUserPosts(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def list(self, request, *args, **kwargs):
#         user_posts = Post.objects.filter(user=request.user.id)
#         print(user_posts)
#         serializer = self.serializer_class(user_posts, many=True)
#         return Response({ "success": True, "posts": serializer.data })


# class LikePost(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer

#     def get(self, request, pk):
#         try:
#             post = Post.objects.get(id=pk)
#             likes_count = PostLike.objects.filter(post=post).count()
#             # serializer = PostLikeSerializer(likes_count, many=True)
#             return Response({ "success": True, "likes":likes_count })


#         except ObjectDoesNotExist:
#             return Response({ "success": False, "message": "post does not exist" })

#     def post(self, request, pk):
#         try:
#             post = Post.objects.get(id=pk)
#             new_post_like = PostLike.objects.get_or_create(user=request.user, post=post)
#             if not new_post_like[1]:
#                 new_post_like[0].delete()
#                 return Response({ "success": True, "message": "post unliked" })
#             else:
#                 return Response({ "success": True, "message": "post liked" })

#         except ObjectDoesNotExist:
#             return Response({ "success": False, "message": "post does not exist" })
    
# class CommentPost(generics.CreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = CommentSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk):
#         try:
#             context = {
#                 "request": request,
#             }
#             post = Post.objects.get(id=pk)
#             comments = PostComment.objects.filter(post=post)
#             print(comments)
#             serializer = self.serializer_class(comments, many=True)
#             return Response({ "success": True, "comments": serializer.data })

#         except ObjectDoesNotExist:
#             return Response({ "success": False, "message": "post does not exist" })

#     def post(self, request, pk):
#         try:
#             context = {
#                 "request": request,
#             }
#             post = Post.objects.get(id=pk)
#             serializer = self.serializer_class(context=context, data=request.data)
#             if serializer.is_valid():
#                 serializer.save(post=post)
#                 return Response({ "success": True, "message": "comment added" })
#             else:
#                 print(serializer.errors)
#                 return Response({ "success": False, "message": "error adding a comment" })

#         except ObjectDoesNotExist:
#             return Response({ "success": False, "message": "post does not exist" })


# Using API Views

class PostListCreateAPIView(APIView):
    def get(self,request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = PostSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            user = request.user
            if user.is_authenticated:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"message":"User must be authenticated "})
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
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostLikeAPIView(APIView):

    def get(self, request, pk):
        post = get_object_or_404(Post,pk=pk)
        likes_count = PostLike.objects.filter(post=post).count()
        return Response({
            "success": True,
            "likes": likes_count
        })

    def post(self, request, pk):
        post = get_object_or_404(PostLike,pk=pk)
        post_like, created = PostLike.objects.get_or_create(user=request.user, post=post)
        if not created:
            post_like.delete()
            return Response({
                "success": True,
                "message": "Post unliked"
            })
        else:
            return Response({
                "success": True,
                "message": "Post liked"
            })
class PostCommentAPIView(APIView):
    def get(self, request, pk):
        post = get_object_or_404(PostComment,pk=pk)
        comments = PostComment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response({
            "success": True,
            "comments": serializer.data
        })

    def post(self, request, pk):
        post = get_object_or_404(PostComment,pk=pk)
        serializer = CommentSerializer(data=request.data, context=self.get_serializer_context())
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
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
