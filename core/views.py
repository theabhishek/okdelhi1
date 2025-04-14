from django.shortcuts import render
from django.db.models import Count
from posts.models import Post
from subreddits.models import Subreddit
from .decorators import django_deprecated_view

@django_deprecated_view(reason="Please use the new home view in the main app instead.")
def home(request):
    # Get the latest posts
    latest_posts = Post.objects.order_by('-created_at')[:5]
    
    # Get the most popular subreddits
    subreddits = Subreddit.objects.filter(approval_status='approved').annotate(
        subscriber_count=Count('subscribers')
    ).order_by('-subscriber_count')[:10]
    
    context = {
        'latest_posts': latest_posts,
        'subreddits': subreddits,
    }
    
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def terms(request):
    return render(request, 'core/terms.html')

def privacy(request):
    return render(request, 'core/privacy.html') 