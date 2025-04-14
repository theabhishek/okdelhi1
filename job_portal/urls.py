from django.urls import path
from . import views

app_name = 'job_portal'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('create/', views.create_job, name='create_job'),
    path('job/<int:pk>/<slug:slug>/', views.job_detail, name='job_detail'),
    path('job/<int:pk>/<slug:slug>/apply/', views.apply_job, name='apply_job'),
    path('pending/', views.pending_jobs, name='pending_jobs'),
    path('job/<int:pk>/<slug:slug>/approve/', views.approve_job, name='approve_job'),
    path('job/<int:pk>/<slug:slug>/reject/', views.reject_job, name='reject_job'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('job/<int:pk>/<slug:slug>/close/', views.close_job, name='close_job'),
    path('job/<int:pk>/<slug:slug>/applications/', views.job_applications, name='job_applications'),
    path('application/<int:pk>/update-status/', views.update_application_status, name='update_application_status'),
    path('notifications/', views.notifications, name='notifications'),
] 