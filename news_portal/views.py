from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import News, NewsComment
from .forms import NewsForm, NewsCommentForm
from django.utils import timezone

def news_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    
    news_list = News.objects.filter(status='APPROVED')
    
    if query:
        news_list = news_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__icontains=query)
        )
    
    if category:
        news_list = news_list.filter(category=category)
    
    paginator = Paginator(news_list, 10)
    page = request.GET.get('page')
    news = paginator.get_page(page)
    
    context = {
        'news': news,
        'categories': News.CATEGORY_CHOICES,
        'query': query,
        'selected_category': category,
    }
    return render(request, 'news_portal/news_list.html', context)

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    comments = news.comments.all()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to comment.')
            return redirect('login')
        
        comment_form = NewsCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.news = news
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been posted.')
            return redirect('news_portal:news_detail', slug=news.slug)
    else:
        comment_form = NewsCommentForm()
    
    news.increment_views()
    
    context = {
        'news': news,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'news_portal/news_detail.html', context)

@login_required
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.status = 'PENDING'
            news.save()
            messages.success(request, 'Your news article has been submitted for review.')
            return redirect('news_portal:my_news')
    else:
        form = NewsForm()
    
    context = {
        'form': form,
        'title': 'Create News Article',
    }
    return render(request, 'news_portal/news_form.html', context)

@login_required
def edit_news(request, slug):
    news = get_object_or_404(News, slug=slug, author=request.user)
    
    if news.status == 'APPROVED':
        messages.warning(request, 'Approved news cannot be edited.')
        return redirect('news_portal:news_detail', slug=news.slug)
    
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            news = form.save(commit=False)
            news.status = 'PENDING'
            news.save()
            messages.success(request, 'Your news article has been updated and submitted for review.')
            return redirect('news_portal:my_news')
    else:
        form = NewsForm(instance=news)
    
    context = {
        'form': form,
        'title': 'Edit News Article',
        'news': news,
    }
    return render(request, 'news_portal/news_form.html', context)

@login_required
def my_news(request):
    news_list = News.objects.filter(author=request.user)
    paginator = Paginator(news_list, 10)
    page = request.GET.get('page')
    news = paginator.get_page(page)
    
    context = {
        'news': news,
    }
    return render(request, 'news_portal/my_news.html', context)

@user_passes_test(lambda u: u.is_superuser)
def pending_news(request):
    news_list = News.objects.filter(status='PENDING')
    paginator = Paginator(news_list, 10)
    page = request.GET.get('page')
    news = paginator.get_page(page)
    
    context = {
        'news': news,
    }
    return render(request, 'news_portal/pending_news.html', context)

@user_passes_test(lambda u: u.is_superuser)
def approve_news(request, slug):
    news = get_object_or_404(News, slug=slug)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            news.status = 'APPROVED'
            news.approved_by = request.user
            news.published_at = timezone.now()
            messages.success(request, 'News article has been approved.')
        elif action == 'reject':
            news.status = 'REJECTED'
            messages.warning(request, 'News article has been rejected.')
        news.save()
        return redirect('news_portal:pending_news')
    
    context = {
        'news': news,
    }
    return render(request, 'news_portal/approve_news.html', context)
