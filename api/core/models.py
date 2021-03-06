import os

from ckeditor_uploader.fields import RichTextUploadingField

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from taggit.managers import TaggableManager


def get_upload_path(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return os.path.join('', filename)


class Post(models.Model):
    h1 = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = RichTextUploadingField()
    image = models.ImageField(upload_to=get_upload_path)
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return f'{self.h1}'


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        related_name='comments'
    )
    username = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_name'
    )
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'{self.post} - {self.text}'


