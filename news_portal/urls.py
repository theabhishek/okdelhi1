from django.urls import path
from . import views

app_name = 'news_portal'

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('create/', views.create_news, name='create_news'),
    path('edit/<slug:slug>/', views.edit_news, name='edit_news'),
    path('my-news/', views.my_news, name='my_news'),
    path('pending/', views.pending_news, name='pending_news'),
    path('approve/<slug:slug>/', views.approve_news, name='approve_news'),
] 