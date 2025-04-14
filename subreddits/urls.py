from django.urls import path
from . import views

app_name = 'subreddits'

urlpatterns = [
    path('', views.subreddit_list, name='list'),
    path('create/', views.create_subreddit, name='create'),
    path('<slug:slug>/', views.subreddit_detail, name='subreddit_detail'),
    path('<slug:slug>/edit/', views.subreddit_edit, name='edit'),
    path('<slug:slug>/subscribe/', views.subscribe, name='subscribe'),
    path('<slug:slug>/unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('approval/', views.subreddit_approval_list, name='approval_list'),
    path('<slug:slug>/approve/', views.approve_subreddit, name='approve'),
    path('<slug:slug>/reject/', views.reject_subreddit, name='reject'),
] 