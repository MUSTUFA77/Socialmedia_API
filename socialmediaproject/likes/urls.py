from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import LikeViewSet

router = DefaultRouter()
router.register('',LikeViewSet)

urlpatterns = [
    path('',include(router.urls))
]