from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.post_create, name='create'),
    path('r/<slug:subreddit_slug>/post/<slug:post_slug>/', views.post_detail, name='detail'),
    path('r/<slug:subreddit_slug>/post/<slug:post_slug>/edit/', views.post_edit, name='edit'),
    path('r/<slug:subreddit_slug>/post/<slug:post_slug>/delete/', views.post_delete, name='delete'),
    path('r/<slug:subreddit_slug>/post/<slug:post_slug>/upvote/', views.post_upvote, name='upvote'),
    path('r/<slug:subreddit_slug>/post/<slug:post_slug>/downvote/', views.post_downvote, name='downvote'),
    path('r/<slug:subreddit_slug>/post/<slug:post_slug>/comment/', views.comment_create, name='comment_create'),
    path('comment/<int:comment_id>/reply/', views.comment_reply, name='comment_reply'),
    path('comment/<int:comment_id>/upvote/', views.comment_upvote, name='comment_upvote'),
    path('comment/<int:comment_id>/downvote/', views.comment_downvote, name='comment_downvote'),
] 