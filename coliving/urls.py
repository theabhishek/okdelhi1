from django.urls import path
from . import views

app_name = 'coliving'

urlpatterns = [
    path('', views.index, name='index'),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:listing_id>/review/', views.add_review, name='add_review'),
] 