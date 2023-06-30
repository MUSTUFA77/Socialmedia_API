from django.urls import path
from .views import UserSignUpAPIView,UserLoginLogoutAPIView,UserDetailAPIView,ChangePasswordAPIView

urlpatterns = [
    path('',UserSignUpAPIView.as_view()),
    path('auth/',UserLoginLogoutAPIView.as_view()),
    path('<int:pk>/',UserDetailAPIView.as_view()),
    path('change-password/',ChangePasswordAPIView.as_view())
]
