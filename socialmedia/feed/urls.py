from django.urls import path
from .views import PostAPIView

app_name = 'feed'

urlpatterns = [
    path('', PostAPIView.as_view(), name='post-list'),
    path('<int:pk>/', PostAPIView.as_view(), name='post-detail'),
    path('<int:pk>/likes/', PostAPIView.as_view(), name='post-likes'),
    path('<int:pk>/comments/', PostAPIView.as_view(), name='post-comments'),
    path('<int:pk>/comments/<int:comment_pk>/', PostAPIView.as_view(), name='post-comment-detail'),
    path('<int:pk>/likes/', PostAPIView.as_view(), {'action': 'likes'}, name='post-likes'),
    path('<int:pk>/comments/', PostAPIView.as_view(), {'action': 'comments'}, name='post-comments'),
]

