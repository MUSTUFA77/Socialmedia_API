from django.urls import path
from .views import PostListCreateAPIView,PostLikeAPIView,PostCommentAPIView,PostDetailAPIView

urlpatterns = [
    path('',PostListCreateAPIView.as_view()),
    path('<int:pk>/',PostDetailAPIView.as_view()),
    path('like/<int:pk>/',PostLikeAPIView.as_view()),
    path('comment/<int:pk>/',PostCommentAPIView.as_view()),
]
