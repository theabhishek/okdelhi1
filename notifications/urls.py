from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('create/', views.create_notification, name='create_notification'),
    path('my-notifications/', views.my_notifications, name='my_notifications'),
    path('notification/<slug:slug>/', views.notification_detail, name='notification_detail'),
    path('pending/', views.pending_notifications, name='pending_notifications'),
    path('approve/<slug:slug>/', views.approve_notification, name='approve_notification'),
] 