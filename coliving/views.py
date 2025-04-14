from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import ColivingSpace, Review

# Create your views here.

def index(request):
    coliving_spaces = ColivingSpace.objects.filter(approval_status='Approved').order_by('-created_at')
    
    # Get filter parameters
    property_type = request.GET.get('property_type')
    gender_preference = request.GET.get('gender_preference')
    city = request.GET.get('city')
    
    # Apply filters
    if property_type:
        coliving_spaces = coliving_spaces.filter(property_type=property_type)
    if gender_preference:
        coliving_spaces = coliving_spaces.filter(gender_preference=gender_preference)
    if city:
        coliving_spaces = coliving_spaces.filter(city__iexact=city)
    
    context = {
        'coliving_spaces': coliving_spaces,
        'property_types': ColivingSpace.PROPERTY_TYPES,
        'gender_preferences': ColivingSpace.GENDER_PREFERENCE,
        'cities': ColivingSpace.objects.values_list('city', flat=True).distinct(),
        'selected_property_type': property_type,
        'selected_gender_preference': gender_preference,
        'selected_city': city,
    }
    return render(request, 'coliving/index.html', context)

def listing_detail(request, listing_id):
    coliving_space = get_object_or_404(ColivingSpace, id=listing_id)
    reviews = Review.objects.filter(coliving_space=coliving_space).order_by('-created_at')
    
    context = {
        'coliving_space': coliving_space,
        'reviews': reviews,
    }
    return render(request, 'coliving/listing_detail.html', context)

@login_required
def add_review(request, listing_id):
    coliving_space = get_object_or_404(ColivingSpace, id=listing_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Check if user has already reviewed this space
        existing_review = Review.objects.filter(coliving_space=coliving_space, user=request.user).first()
        if existing_review:
            messages.error(request, 'You have already reviewed this coliving space.')
            return redirect('coliving:listing_detail', listing_id=listing_id)
        
        # Create new review
        review = Review.objects.create(
            coliving_space=coliving_space,
            user=request.user,
            rating=rating,
            comment=comment
        )
        messages.success(request, 'Your review has been added successfully!')
        return redirect('coliving:listing_detail', listing_id=listing_id)
    
    return render(request, 'coliving/add_review.html', {
        'coliving_space': coliving_space
    })
