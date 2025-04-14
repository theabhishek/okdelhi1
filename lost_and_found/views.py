from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .models import LostAndFoundItem
from .forms import LostAndFoundItemForm

def is_superuser(user):
    return user.is_superuser

@login_required
def create_item(request):
    if request.method == 'POST':
        form = LostAndFoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'Your item has been submitted for approval.')
            return redirect('lost_and_found:item_list')
    else:
        form = LostAndFoundItemForm()
    return render(request, 'lost_and_found/create_item.html', {'form': form})

def item_list(request):
    query = request.GET.get('q')
    lost_items = LostAndFoundItem.objects.filter(item_type='LOST', status='APPROVED', is_resolved=False)
    found_items = LostAndFoundItem.objects.filter(item_type='FOUND', status='APPROVED', is_resolved=False)
    
    if query:
        lost_items = lost_items.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(contact_number__icontains=query)
        )
        found_items = found_items.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(contact_number__icontains=query)
        )
    
    paginator_lost = Paginator(lost_items, 10)
    paginator_found = Paginator(found_items, 10)
    
    page_number = request.GET.get('page')
    lost_page_obj = paginator_lost.get_page(page_number)
    found_page_obj = paginator_found.get_page(page_number)
    
    return render(request, 'lost_and_found/item_list.html', {
        'lost_items': lost_page_obj,
        'found_items': found_page_obj,
        'query': query
    })

@login_required
def my_items(request):
    items = LostAndFoundItem.objects.filter(user=request.user)
    return render(request, 'lost_and_found/my_items.html', {'items': items})

@user_passes_test(is_superuser)
def admin_approval(request):
    items = LostAndFoundItem.objects.filter(status='PENDING')
    return render(request, 'lost_and_found/admin_approval.html', {'items': items})

@user_passes_test(is_superuser)
def approve_item(request, pk):
    item = get_object_or_404(LostAndFoundItem, pk=pk)
    item.status = 'APPROVED'
    item.approved_at = timezone.now()
    item.approved_by = request.user
    item.save()
    messages.success(request, 'Item has been approved.')
    return redirect('lost_and_found:admin_approval')

@user_passes_test(is_superuser)
def reject_item(request, pk):
    item = get_object_or_404(LostAndFoundItem, pk=pk)
    item.status = 'REJECTED'
    item.save()
    messages.warning(request, 'Item has been rejected.')
    return redirect('lost_and_found:admin_approval')

@login_required
def mark_resolved(request, pk):
    item = get_object_or_404(LostAndFoundItem, pk=pk)
    if item.user == request.user or request.user.is_superuser:
        item.is_resolved = True
        item.save()
        messages.success(request, 'Item has been marked as resolved.')
    return redirect('lost_and_found:item_list')
