from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import Coupon, Click
from .forms import CouponForm
from django.db.models import Q
from django.urls import reverse

def is_superuser(user):
    return user.is_superuser

def coupon_list(request):
    query = request.GET.get('q')
    coupons = Coupon.objects.filter(is_active=True)
    
    if query:
        coupons = coupons.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(store__icontains=query)
        )
    
    paginator = Paginator(coupons, 9)  # Show 9 coupons per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'coupon_service/coupon_list.html', {
        'page_obj': page_obj,
    })

@login_required
@user_passes_test(is_superuser)
def create_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST, request.FILES)
        if form.is_valid():
            coupon = form.save(commit=False)
            coupon.created_by = request.user
            coupon.save()
            messages.success(request, 'Coupon created successfully!')
            return redirect('coupon_service:coupon_list')
    else:
        form = CouponForm()
    return render(request, 'coupon_service/create_coupon.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def edit_coupon(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        form = CouponForm(request.POST, request.FILES, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coupon updated successfully!')
            return redirect('coupon_service:coupon_list')
    else:
        form = CouponForm(instance=coupon)
    return render(request, 'coupon_service/edit_coupon.html', {'form': form, 'coupon': coupon})
@login_required
def track_click(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    
    # Create click record
    Click.objects.create(
        coupon=coupon,
        user=request.user if request.user.is_authenticated else None,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    # Redirect to the affiliate link
    return HttpResponseRedirect(coupon.affiliate_link)

@login_required
@user_passes_test(is_superuser)
def coupon_stats(request):
    coupons = Coupon.objects.all().order_by('-created_at')
    stats = []
    for coupon in coupons:
        click_count = coupon.clicks.count()
        stats.append({
            'coupon': coupon,
            'click_count': click_count,
            'unique_users': coupon.clicks.values('user').distinct().count(),
        })
    return render(request, 'coupon_service/stats.html', {'stats': stats})
