from django.urls import path
from . import views

app_name = 'storytelling'

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('create/', views.create_story, name='create_story'),
    path('story/<int:pk>/', views.story_detail, name='story_detail'),
    path('story/<int:pk>/like/', views.like_story, name='like_story'),
    path('pending/', views.pending_stories, name='pending_stories'),
    path('story/<int:pk>/approve/', views.approve_story, name='approve_story'),
    path('story/<int:pk>/reject/', views.reject_story, name='reject_story'),
    path('my-stories/', views.my_stories, name='my_stories'),
] 