from django.urls import path
from . import views

app_name = 'hotel_service'

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('create/', views.hotel_create, name='hotel_create'),
    path('<int:pk>/', views.hotel_detail, name='hotel_detail'),
    path('<int:pk>/edit/', views.hotel_edit, name='hotel_edit'),
    path('<int:pk>/delete/', views.hotel_delete, name='hotel_delete'),
] 