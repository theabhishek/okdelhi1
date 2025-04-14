from django.contrib import admin
from .models import Coupon, Click

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['title', 'store', 'affiliate_link', 'valid_from', 'valid_until', 'is_active', 'created_by']
    list_filter = ['store', 'is_active', 'valid_from', 'valid_until']
    search_fields = ['title', 'description', 'store']
    readonly_fields = ['created_by', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'

    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by for new objects
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ['coupon', 'user', 'ip_address', 'clicked_at']
    list_filter = ['clicked_at']
    search_fields = ['coupon__title', 'user__username', 'ip_address']
    readonly_fields = ['coupon', 'user', 'ip_address', 'clicked_at', 'user_agent']
    date_hierarchy = 'clicked_at'
