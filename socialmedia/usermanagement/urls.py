from django.urls import path
from .views import UserSignUpAPIView,UserLoginLogoutAPIView,UserDetailAPIView

urlpatterns = [
    path('',UserSignUpAPIView.as_view()),
    path('Auth/',UserLoginLogoutAPIView.as_view()),
    path('<int:pk>/',UserDetailAPIView.as_view())
]
