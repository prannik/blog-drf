from rest_framework import viewsets, permissions, pagination
from .serialzers import PostSerializer
from .models import Post
from rest_framework.response import Response


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    ordering = 'created_at'

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination

