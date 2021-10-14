from django.contrib import admin

from .models import Comment, Post


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('h1', ), }


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
