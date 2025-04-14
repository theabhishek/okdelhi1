from django.contrib import admin
from .models import Subreddit

class SubredditAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'created_at', 'approval_status')
    list_filter = ('approval_status', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'creator')
        }),
        ('Approval', {
            'fields': ('approval_status', 'approved_by', 'approved_at')
        }),
        ('Media', {
            'fields': ('icon', 'banner')
        }),
        ('Members', {
            'fields': ('moderators', 'subscribers')
        }),
    )
    raw_id_fields = ('creator', 'approved_by', 'moderators', 'subscribers')

admin.site.register(Subreddit, SubredditAdmin) 