from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'subreddit', 'created_at', 'score')
    list_filter = ('created_at', 'subreddit')
    search_fields = ('title', 'content', 'author__username', 'subreddit__name')
    readonly_fields = ('created_at', 'score')
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content', 'author', 'subreddit')
        }),
        ('Media', {
            'fields': ('image', 'url')
        }),
        ('Metadata', {
            'fields': ('created_at', 'score')
        }),
    )
    raw_id_fields = ('author', 'subreddit')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'score')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('created_at', 'score')
    raw_id_fields = ('author', 'post', 'parent') 