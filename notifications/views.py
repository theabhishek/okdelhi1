from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils import timezone
from .models import Notification, NotificationComment
from .forms import NotificationForm, NotificationCommentForm, NotificationApprovalForm

@login_required
def create_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.author = request.user
            notification.save()
            messages.success(request, 'Notification created successfully and is pending approval.')
            return redirect('notifications:my_notifications')
    else:
        form = NotificationForm()
    return render(request, 'notifications/create_notification.html', {'form': form})

@login_required
def my_notifications(request):
    notifications = Notification.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'notifications/my_notifications.html', {'notifications': notifications})

@login_required
def notification_detail(request, slug):
    notification = get_object_or_404(Notification, slug=slug)
    comments = notification.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        comment_form = NotificationCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.notification = notification
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('notifications:notification_detail', slug=slug)
    else:
        comment_form = NotificationCommentForm()
    
    return render(request, 'notifications/notification_detail.html', {
        'notification': notification,
        'comments': comments,
        'comment_form': comment_form
    })

@permission_required('notifications.can_approve_notification')
def pending_notifications(request):
    notifications = Notification.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'notifications/pending_notifications.html', {'notifications': notifications})

@permission_required('notifications.can_approve_notification')
def approve_notification(request, slug):
    notification = get_object_or_404(Notification, slug=slug)
    
    if request.method == 'POST':
        form = NotificationApprovalForm(request.POST, instance=notification)
        if form.is_valid():
            notification = form.save(commit=False)
            if notification.status == 'approved':
                notification.approved_at = timezone.now()
                notification.approved_by = request.user
            notification.save()
            messages.success(request, f'Notification has been {notification.status}.')
            return redirect('notifications:pending_notifications')
    else:
        form = NotificationApprovalForm(instance=notification)
    
    return render(request, 'notifications/approve_notification.html', {
        'notification': notification,
        'form': form
    })

def notification_list(request):
    notifications = Notification.objects.filter(
        status='approved',
        is_active=True
    ).order_by('-priority', '-created_at')
    
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})
