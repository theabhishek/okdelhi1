from django.contrib import admin
from .models import PGListing, PGImage, Booking, Review

class PGImageInline(admin.TabularInline):
    model = PGImage
    extra = 1

@admin.register(PGListing)
class PGListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'property_type', 'price_per_month', 'locality', 'city', 'approval_status', 'created_at')
    list_filter = ('property_type', 'approval_status', 'city', 'gender_preference', 'created_at')
    search_fields = ('title', 'description', 'locality', 'city')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PGImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'owner', 'property_type', 'price_per_month')
        }),
        ('Preferences', {
            'fields': ('gender_preference',)
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

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('pg_listing', 'user', 'check_in_date', 'check_out_date', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'check_in_date', 'check_out_date')
    search_fields = ('pg_listing__title', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pg_listing', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('pg_listing__title', 'user__username', 'comment')
    readonly_fields = ('created_at',)
