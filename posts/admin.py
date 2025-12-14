from django.contrib import admin

from .models import Author, Category, Post, Comment, PostLike, Favourite

admin.site.register(Favourite)
