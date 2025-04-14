from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Subreddit
from .forms import SubredditCreateForm, SubredditUpdateForm
from users.models import CustomUser
from core.decorators import django_deprecated_view

def is_superadmin(user):
    return user.is_superuser

def subreddit_list(request):
    if request.user.is_superuser:
        subreddits = Subreddit.objects.all()
    else:
        subreddits = Subreddit.objects.filter(approval_status='approved')
    return render(request, 'subreddits/list.html', {'subreddits': subreddits})

@django_deprecated_view(reason="This view is deprecated. Please use the new community creation flow.")
@login_required
def create_subreddit(request):
    if request.method == 'POST':
        form = SubredditCreateForm(request.POST, request.FILES)
        if form.is_valid():
            subreddit = form.save(commit=False)
            subreddit.creator = request.user
            subreddit.save()
            subreddit.moderators.add(request.user)
            subreddit.subscribers.add(request.user)
            messages.success(request, 'Community created successfully!')
            return redirect('subreddits:subreddit_detail', slug=subreddit.slug)
    else:
        form = SubredditCreateForm()
    return render(request, 'subreddits/create_subreddit.html', {'form': form})

@login_required
def subreddit_detail(request, slug):
    subreddit = get_object_or_404(Subreddit, slug=slug)
    if not subreddit.is_approved() and not request.user.is_superuser:
        messages.error(request, 'This subreddit is pending approval.')
        return redirect('home')
    context = {
        'subreddit': subreddit,
        'is_subscribed': request.user.is_authenticated and subreddit.subscribers.filter(id=request.user.id).exists(),
        'subscriber_count': subreddit.get_member_count(),
        'is_moderator': request.user.is_authenticated and subreddit.moderators.filter(id=request.user.id).exists()
    }
    return render(request, 'subreddits/detail.html', context)

@login_required
def subreddit_edit(request, slug):
    subreddit = get_object_or_404(Subreddit, slug=slug)
    if request.user not in subreddit.moderators.all():
        messages.error(request, 'You do not have permission to edit this subreddit.')
        return redirect('subreddits:detail', slug=slug)
    
    if request.method == 'POST':
        form = SubredditUpdateForm(request.POST, request.FILES, instance=subreddit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subreddit updated successfully!')
            return redirect('subreddits:detail', slug=slug)
    else:
        form = SubredditUpdateForm(instance=subreddit)
    return render(request, 'subreddits/edit.html', {'form': form, 'subreddit': subreddit})

@login_required
@user_passes_test(is_superadmin)
def subreddit_approval_list(request):
    pending_subreddits = Subreddit.objects.filter(approval_status='pending')
    return render(request, 'subreddits/approval_list.html', {
        'pending_subreddits': pending_subreddits
    })

@login_required
@user_passes_test(is_superadmin)
def approve_subreddit(request, slug):
    subreddit = get_object_or_404(Subreddit, slug=slug)
    if request.method == 'POST':
        subreddit.approval_status = 'approved'
        subreddit.approved_by = request.user
        subreddit.approved_at = timezone.now()
        subreddit.save()
        messages.success(request, f'Subreddit "{subreddit.name}" has been approved.')
    return redirect('home')

@login_required
@user_passes_test(is_superadmin)
def reject_subreddit(request, slug):
    subreddit = get_object_or_404(Subreddit, slug=slug)
    if request.method == 'POST':
        subreddit.approval_status = 'rejected'
        subreddit.approved_by = request.user
        subreddit.approved_at = timezone.now()
        subreddit.save()
        messages.warning(request, f'Subreddit "{subreddit.name}" has been rejected.')
    return redirect('home')

@login_required
def subscribe(request, slug):
    subreddit = get_object_or_404(Subreddit, slug=slug)
    if subreddit.is_pending():
        messages.warning(request, 'Cannot subscribe to a pending subreddit.')
        return redirect('home')
    subreddit.subscribers.add(request.user)
    messages.success(request, f'Successfully subscribed to r/{subreddit.name}')
    return redirect('home')

@login_required
def unsubscribe(request, slug):
    subreddit = get_object_or_404(Subreddit, slug=slug)
    subreddit.subscribers.remove(request.user)
    messages.success(request, f'Successfully unsubscribed from r/{subreddit.name}')
    return redirect('home') 