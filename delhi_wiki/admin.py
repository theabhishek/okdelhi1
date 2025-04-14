from django.contrib import admin
from .models import Area, Landmark, FoodPlace, Market, Event, LandmarkReview, FoodPlaceReview, MarketReview

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_verified', 'created_by', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('name', 'location', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Landmark)
class LandmarkAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'category', 'rating', 'is_verified', 'created_by', 'created_at')
    list_filter = ('category', 'is_verified', 'area', 'created_at')
    search_fields = ('name', 'description', 'address')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

@admin.register(FoodPlace)
class FoodPlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'cuisine', 'rating', 'is_verified', 'created_by', 'created_at')
    list_filter = ('cuisine', 'is_verified', 'area', 'created_at')
    search_fields = ('name', 'description', 'address')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'is_verified', 'created_by', 'created_at')
    list_filter = ('is_verified', 'area', 'created_at')
    search_fields = ('name', 'description', 'address')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'area', 'category', 'start_date', 'end_date', 'is_verified', 'created_by', 'created_at')
    list_filter = ('category', 'is_verified', 'area', 'start_date', 'end_date')
    search_fields = ('title', 'description', 'venue')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')

@admin.register(LandmarkReview)
class LandmarkReviewAdmin(admin.ModelAdmin):
    list_display = ('landmark', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('content', 'landmark__name', 'author__username')

@admin.register(FoodPlaceReview)
class FoodPlaceReviewAdmin(admin.ModelAdmin):
    list_display = ('food_place', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('content', 'food_place__name', 'author__username')

@admin.register(MarketReview)
class MarketReviewAdmin(admin.ModelAdmin):
    list_display = ('market', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('content', 'market__name', 'author__username')
