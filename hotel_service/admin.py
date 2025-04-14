from django.contrib import admin
from .models import Hotel

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel_type', 'location', 'city', 'price_range', 'is_approved', 'created_by', 'created_at')
    list_filter = ('hotel_type', 'city', 'is_approved', 'created_at')
    search_fields = ('name', 'location', 'city', 'description')
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'hotel_type', 'description', 'price_range')
        }),
        ('Location', {
            'fields': ('address', 'location', 'city')
        }),
        ('Contact Information', {
            'fields': ('contact_number', 'email', 'website')
        }),
        ('Booking Information', {
            'fields': ('affiliate_link', 'check_in_time', 'check_out_time', 'amenities')
        }),
        ('Administrative', {
            'fields': ('is_approved', 'created_by', 'created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change) 