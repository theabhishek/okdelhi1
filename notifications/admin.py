from django.contrib import admin
from .models import Notification, NotificationComment

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'priority', 'created_at', 'approved_at', 'is_active')
    list_filter = ('status', 'priority', 'created_at', 'is_active')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'approved_at', 'approved_by')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'content', 'author', 'priority')
        }),
        ('Status and Dates', {
            'fields': ('status', 'start_date', 'end_date', 'is_active')
        }),
        ('Approval Information', {
            'fields': ('approved_at', 'approved_by'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(NotificationComment)
class NotificationCommentAdmin(admin.ModelAdmin):
    list_display = ('notification', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'notification__title')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
