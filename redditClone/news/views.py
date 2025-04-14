from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db import models
from .models import News

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
        'news_list': page_obj.object_list,  # Pass the actual list of news items
        'page_obj': page_obj,  # Pass the pagination object
        'is_paginated': page_obj.has_other_pages(),  # Pass pagination status
        'query': query  # Pass the search query
    })

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk, is_published=True)
    news.increment_views()
    return render(request, 'news/news_detail.html', {'news': news}) 