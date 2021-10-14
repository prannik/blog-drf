from django.core.mail import send_mail

from rest_framework import filters, generics, pagination, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from taggit.models import Tag

from . import models, serialzers


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    ordering = 'created_at'


class PostViewSet(viewsets.ModelViewSet):
    search_fields = ['content', 'h1']
    filter_backends = (filters.SearchFilter,)
    serializer_class = serialzers.PostSerializer
    queryset = models.Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


class TagDetailView(generics.ListAPIView):
    serializer_class = serialzers.PostSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return models.Post.objects.filter(tags=tag)


class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = serialzers.TagSerializer
    permission_classes = [permissions.AllowAny]


class AsideView(generics.ListAPIView):
    queryset = models.Post.objects.all().order_by('-id')[:5]
    serializer_class = serialzers.PostSerializer
    permission_classes = [permissions.AllowAny]


class FeedBackView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serialzers.ContactSerailizer

    def post(self, request,):
        serializer_class = serialzers.ContactSerailizer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(
                f'От {name} | {subject}', message,
                from_email, ['prannik.m@gmail.com']
            )
            return Response({"success": "Sent"})


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serialzers.RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": serialzers.UserSerializer(
                user,
                context=self.get_serializer_context()).data,
            "message": "Пользователь успешно создан",
        })


class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serialzers.UserSerializer

    def get(self, request):
        return Response({
            "user": serialzers.UserSerializer(
                request.user,
                context=self.get_serializer_context()).data,
        })


class CommentView(generics.ListCreateAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serialzers.CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_slug = self.kwargs['post_slug'].lower()
        post = models.Post.objects.get(slug=post_slug)
        return models.Comment.objects.filter(post=post)
