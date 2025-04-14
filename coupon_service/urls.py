from django.urls import path
from . import views

app_name = 'coupon_service'

urlpatterns = [
    path('', views.coupon_list, name='coupon_list'),
    path('create/', views.create_coupon, name='create_coupon'),
    path('edit/<int:pk>/', views.edit_coupon, name='edit_coupon'),
    path('click/<int:pk>/', views.track_click, name='track_click'),
    path('stats/', views.coupon_stats, name='coupon_stats'),
] 