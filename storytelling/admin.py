from django.contrib import admin
from .models import Story

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at', 'approved_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at', 'approved_at')
    actions = ['approve_stories', 'reject_stories']

    def approve_stories(self, request, queryset):
        for story in queryset:
            story.approve(request.user)
        self.message_user(request, f"{queryset.count()} stories were successfully approved.")
    approve_stories.short_description = "Approve selected stories"

    def reject_stories(self, request, queryset):
        for story in queryset:
            story.reject(request.user)
        self.message_user(request, f"{queryset.count()} stories were successfully rejected.")
    reject_stories.short_description = "Reject selected stories"
