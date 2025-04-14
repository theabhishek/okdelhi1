from django.urls import path
from . import views

app_name = 'static_pages'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('test-cloudinary/', views.test_cloudinary, name='test_cloudinary'),
] 