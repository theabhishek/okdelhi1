from django.urls import path
from . import views

app_name = 'medical'

urlpatterns = [
    path('', views.medical_facility_list, name='facility_list'),
    path('create/', views.medical_facility_create, name='facility_create'),
    path('<int:pk>/', views.medical_facility_detail, name='facility_detail'),
    path('<int:pk>/edit/', views.medical_facility_edit, name='facility_edit'),
    path('<int:pk>/delete/', views.medical_facility_delete, name='facility_delete'),
] 