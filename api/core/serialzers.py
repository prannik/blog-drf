import taggit_serializer.serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from taggit.models import Tag

from .models import Comment, Post


class PostSerializer(taggit_serializer.serializers.TaggitSerializer, serializers.ModelSerializer):

    tags = taggit_serializer.serializers.TagListSerializerField()
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Post
        fields = (
            'id', 'h1', 'slug',
            'title', 'content',
            'image', 'created_at',
            'author', 'tags'
        )
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


class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password2',

        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        password2 = validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({
                'password': 'Passwords do not match'
            })
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    username = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all()
    )
    post = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Post.objects.all()
    )

    class Meta:
        model = Comment
        fields = (
            "id", "post", "username",
            "text", "created_date"
        )
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }
