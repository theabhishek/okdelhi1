from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import News
from django.db import models

def news_list(request):
    # Get all published news articles
    news_list = News.objects.filter(is_published=True).order_by('-created_at')
    
    # Handle search
    query = request.GET.get('q')
    if query:
        news_list = news_list.filter(
            models.Q(title__icontains=query) |
            models.Q(content__icontains=query) |
            models.Q(author__username__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news/news_list.html', {
        'page_obj': page_obj,
        'query': query
    })

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk, is_published=True)
    news.increment_views()
    return render(request, 'news/news_detail.html', {'news': news}) 