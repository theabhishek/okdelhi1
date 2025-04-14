from django.contrib import admin
from .models import LostAndFoundItem

@admin.register(LostAndFoundItem)
class LostAndFoundItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'item_type', 'status', 'user', 'created_at', 'approved_at')
    list_filter = ('item_type', 'status', 'created_at', 'approved_at')
    search_fields = ('title', 'description', 'location', 'user__username')
    readonly_fields = ('created_at', 'approved_at', 'approved_by')
    fieldsets = (
        ('Item Information', {
            'fields': ('user', 'item_type', 'title', 'description', 'location', 'date_lost_found', 'contact_number', 'image')
        }),
        ('Status Information', {
            'fields': ('status', 'approved_at', 'approved_by')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
