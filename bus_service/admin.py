from django.contrib import admin
from .models import (
    Agency, Route, Stop, Trip, StopTime,
    FareAttribute, FareRule, UserFareHistory
)

@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('agency_id', 'agency_name', 'agency_url', 'agency_timezone')
    search_fields = ('agency_name', 'agency_id')

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('route_id', 'route_short_name', 'route_long_name', 'route_type', 'agency')
    list_filter = ('route_type', 'agency')
    search_fields = ('route_short_name', 'route_long_name', 'route_id')

@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ('stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'wheelchair_boarding')
    search_fields = ('stop_name', 'stop_id', 'stop_code')
    list_filter = ('wheelchair_boarding',)

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('trip_id', 'route', 'trip_headsign', 'direction_id')
    list_filter = ('route', 'direction_id', 'wheelchair_accessible', 'bikes_allowed')
    search_fields = ('trip_id', 'trip_headsign')

@admin.register(StopTime)
class StopTimeAdmin(admin.ModelAdmin):
    list_display = ('trip', 'stop', 'arrival_time', 'departure_time', 'stop_sequence')
    list_filter = ('trip__route', 'stop')
    search_fields = ('trip__trip_id', 'stop__stop_name')

@admin.register(FareAttribute)
class FareAttributeAdmin(admin.ModelAdmin):
    list_display = ('fare_id', 'price', 'currency_type', 'payment_method', 'transfers')
    search_fields = ('fare_id',)

@admin.register(FareRule)
class FareRuleAdmin(admin.ModelAdmin):
    list_display = ('fare', 'route', 'origin_id', 'destination_id')
    list_filter = ('route',)
    search_fields = ('fare__fare_id', 'route__route_short_name')

@admin.register(UserFareHistory)
class UserFareHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'origin_stop', 'destination_stop', 'fare', 'journey_date', 'payment_status')
    list_filter = ('payment_status', 'journey_date', 'route')
    search_fields = ('user__username', 'origin_stop__stop_name', 'destination_stop__stop_name')
