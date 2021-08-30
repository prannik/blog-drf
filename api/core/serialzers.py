from rest_framework import serializers
from .models import Post
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from taggit.models import Tag
from django.contrib.auth.models import User


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ('id', 'h1', 'slug', 'title', 'content', 'image', 'created_at', 'author', 'tags')
        lookup_fields = 'slug'
        extra_kwargs = {
            'url': {'lookup_fields': 'slug'}
        }

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name',)
        lookup_fields = 'name'
        extra_kwargs = {
            'url': {'lookup_fields': 'name'}
        }

class ContactSerailizer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    subject = serializers.CharField()
    message = serializers.CharField()

