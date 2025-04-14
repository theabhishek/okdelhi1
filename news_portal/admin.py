from django.contrib import admin
from .models import News, NewsComment

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at', 'published_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'news__title')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
