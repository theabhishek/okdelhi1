from django.urls import path
from . import views

app_name = 'metro'

urlpatterns = [
    path('', views.metro_home, name='metro_home'),
    path('route-finder/', views.metro_route_finder, name='metro_route_finder'),
    path('stations/', views.metro_station_list, name='metro_station_list'),
    path('stations/<slug:slug>/', views.metro_station_detail, name='metro_station_detail'),
] 