from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('h1', ), }


admin.site.register(Post, PostAdmin)
