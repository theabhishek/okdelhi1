from django.urls import path
from . import views

app_name = 'pg_rental'

urlpatterns = [
    path('', views.pg_listings, name='listings'),
    path('listing/<int:pk>/', views.pg_detail, name='pg_detail'),
    path('listing/add/', views.add_listing, name='add_listing'),
    path('listing/<int:pk>/review/', views.add_review, name='add_review'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('my-listings/', views.my_listings, name='my_listings'),
] 