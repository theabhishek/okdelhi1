from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Story
from .forms import StoryForm
from django.db import models

def is_superuser(user):
    return user.is_superuser

def story_list(request):
    stories = Story.objects.filter(status='APPROVED').order_by('-created_at')
    
    # Handle search
    query = request.GET.get('q')
    if query:
        stories = stories.filter(
            models.Q(title__icontains=query) |
            models.Q(content__icontains=query) |
            models.Q(location__icontains=query) |
            models.Q(author__username__icontains=query)
        )
    
    paginator = Paginator(stories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'storytelling/story_list.html', {
        'page_obj': page_obj,
        'query': query
    })

@login_required
def create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            messages.success(request, 'Your story has been submitted for approval!')
            return redirect('storytelling:story_list')
    else:
        form = StoryForm()
    return render(request, 'storytelling/create_story.html', {'form': form})

def story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if story.status != 'APPROVED' and not (request.user.is_superuser or request.user == story.author):
        messages.error(request, 'This story is not available.')
        return redirect('storytelling:story_list')
    
    story.views += 1
    story.save()
    return render(request, 'storytelling/story_detail.html', {'story': story})

@login_required
@user_passes_test(is_superuser)
def pending_stories(request):
    stories = Story.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'storytelling/pending_stories.html', {'stories': stories})

@login_required
@user_passes_test(is_superuser)
def approve_story(request, pk):
    story = get_object_or_404(Story, pk=pk)
    story.approve(request.user)
    messages.success(request, f'Story "{story.title}" has been approved.')
    return redirect('storytelling:pending_stories')

@login_required
@user_passes_test(is_superuser)
def reject_story(request, pk):
    story = get_object_or_404(Story, pk=pk)
    story.reject(request.user)
    messages.success(request, f'Story "{story.title}" has been rejected.')
    return redirect('storytelling:pending_stories')

@login_required
def my_stories(request):
    stories = Story.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'storytelling/my_stories.html', {'stories': stories})

@login_required
def like_story(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if request.user in story.likes.all():
        story.likes.remove(request.user)
        action = 'unliked'
    else:
        story.likes.add(request.user)
        action = 'liked'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'action': action,
            'likes_count': story.likes.count()
        })
    
    return redirect('storytelling:story_detail', pk=pk)
