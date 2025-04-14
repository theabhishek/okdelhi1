from django.contrib import admin
from .models import ColivingSpace

@admin.register(ColivingSpace)
class ColivingSpaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'price_per_month', 'locality', 'city', 'approval_status', 'created_at')
    list_filter = ('approval_status', 'city', 'created_at')
    search_fields = ('title', 'description', 'locality', 'city')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'owner', 'price_per_month')
        }),
        ('Location', {
            'fields': ('locality', 'city', 'state', 'pincode')
        }),
        ('Status', {
            'fields': ('is_active', 'approval_status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
