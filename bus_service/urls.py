from django.urls import path
from . import views

app_name = 'bus_service'

urlpatterns = [
    path('', views.route_search, name='route_search'),
    path('search/', views.route_search, name='route_search'),
    path('calculate-fare/', views.calculate_fare, name='calculate_fare'),
    path('fare-history/', views.fare_history, name='fare_history'),
    path('stops/search/', views.search_stops, name='search_stops'),
    path('route/<str:route_id>/', views.route_detail, name='route_detail'),
] 