from rest_framework import viewsets,filters
from .models import Post
from .serializers import PostSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter,filters.SearchFilter]
    search_fields = ['title','tags']
    ordering_fields =[''] 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

