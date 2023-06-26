from django.urls import path
from .views import UserListCreateAPIView,UserLoginAPIView,UserDetailAPIView

urlpatterns = [
    path('',UserListCreateAPIView.as_view()),
    path('login/',UserLoginAPIView.as_view()),
    path('<int:pk>/',UserDetailAPIView.as_view())
]
