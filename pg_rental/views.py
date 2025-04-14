from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import PGListing, Booking, Review, PGImage
from .forms import PGListingForm, BookingForm, ReviewForm

def is_superuser(user):
    return user.is_superuser

def pg_listings(request):
    query = request.GET.get('q', '')
    property_type = request.GET.get('property_type', '')
    gender_preference = request.GET.get('gender_preference', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    listings = PGListing.objects.filter(is_active=True, approval_status='Approved')
    
    if query:
        listings = listings.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(locality__icontains=query) |
            Q(city__icontains=query)
        )
    
    if property_type:
        listings = listings.filter(property_type=property_type)
    
    if gender_preference:
        listings = listings.filter(gender_preference=gender_preference)
    
    if min_price:
        listings = listings.filter(price_per_month__gte=min_price)
    
    if max_price:
        listings = listings.filter(price_per_month__lte=max_price)
    
    paginator = Paginator(listings, 12)
    page = request.GET.get('page')
    listings = paginator.get_page(page)
    
    context = {
        'listings': listings,
        'property_types': PGListing.PROPERTY_TYPES,
        'gender_preferences': PGListing.GENDER_PREFERENCE,
    }
    return render(request, 'pg_rental/listings.html', context)

def pg_detail(request, pk):
    listing = get_object_or_404(PGListing, pk=pk)
    images = listing.images.all()
    reviews = Review.objects.filter(pg_listing=listing)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to book this PG.')
            return redirect('users:login')
            
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        
        if not name or not mobile:
            messages.error(request, 'Please provide your name and mobile number.')
            return redirect('pg_rental:pg_detail', pk=pk)
            
        # Create booking with today's date as check-in and 30 days later as check-out
        from datetime import datetime, timedelta
        today = datetime.now().date()
        thirty_days_later = today + timedelta(days=30)
        
        booking = Booking.objects.create(
            pg_listing=listing,
            user=request.user,
            name=name,
            mobile=mobile,
            check_in_date=today,
            check_out_date=thirty_days_later,
            total_amount=listing.price_per_month,
            status='Pending'
        )
        
        messages.success(request, 'Booking request submitted successfully! The owner will contact you shortly.')
        return redirect('pg_rental:pg_detail', pk=pk)
    
    context = {
        'listing': listing,
        'images': images,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'pg_rental/detail.html', context)

@login_required
def add_listing(request):
    if request.method == 'POST':
        form = PGListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            form.save_m2m()
            
            # Handle multiple images
            for i in range(1, 6):
                image_field = f'image{i}'
                if image_field in request.FILES:
                    image = request.FILES[image_field]
                    PGImage.objects.create(
                        pg_listing=listing,
                        image=image,
                        is_primary=(i == 1)
                    )
            
            messages.success(request, 'PG listing added successfully!')
            return redirect('pg_rental:pg_detail', pk=listing.pk)
    else:
        form = PGListingForm()
    
    context = {'form': form}
    return render(request, 'pg_rental/add_listing.html', context)

@login_required
def add_review(request, pk):
    listing = get_object_or_404(PGListing, pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.pg_listing = listing
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('pg_rental:pg_detail', pk=pk)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'listing': listing,
    }
    return render(request, 'pg_rental/add_review.html', context)

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    context = {'bookings': bookings}
    return render(request, 'pg_rental/my_bookings.html', context)

@login_required
def my_listings(request):
    listings = PGListing.objects.filter(owner=request.user)
    context = {'listings': listings}
    return render(request, 'pg_rental/my_listings.html', context)

@login_required
@user_passes_test(is_superuser)
def manage_approvals(request):
    pending_listings = PGListing.objects.filter(approval_status='Pending')
    approved_listings = PGListing.objects.filter(approval_status='Approved')
    rejected_listings = PGListing.objects.filter(approval_status='Rejected')
    
    context = {
        'pending_listings': pending_listings,
        'approved_listings': approved_listings,
        'rejected_listings': rejected_listings,
    }
    return render(request, 'pg_rental/manage_approvals.html', context)

@login_required
@user_passes_test(is_superuser)
def update_approval(request, listing_id):
    listing = get_object_or_404(PGListing, id=listing_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Approved', 'Rejected']:
            listing.approval_status = new_status
            listing.save()
            messages.success(request, f'Listing {listing.title} has been {new_status.lower()}.')
        return redirect('pg_rental:manage_approvals')
    return redirect('pg_rental:manage_approvals')
