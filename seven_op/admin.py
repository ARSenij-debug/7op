from django.contrib import admin

# Register your models here.

from .models import Category, UploadedFile, UploadedPhoto, Post, BlogAuthor, Blog, Comment, Paragraph

admin.site.register(Paragraph)
admin.site.register(Category)
admin.site.register(UploadedFile)
admin.site.register(UploadedPhoto)
admin.site.register(Post)
admin.site.register(BlogAuthor)
admin.site.register(Blog)
admin.site.register(Comment)
