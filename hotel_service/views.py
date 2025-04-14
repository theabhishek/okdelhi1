from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from .models import Hotel

def hotel_list(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    hotel_type = request.GET.get('type', '')
    price_range = request.GET.get('price', '')
    
    hotels = Hotel.objects.filter(is_approved=True)
    
    if query:
        hotels = hotels.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(amenities__icontains=query)
        )
    
    if location:
        hotels = hotels.filter(
            Q(location__icontains=location) |
            Q(city__icontains=location)
        )
    
    if hotel_type:
        hotels = hotels.filter(hotel_type=hotel_type)
    
    if price_range:
        hotels = hotels.filter(price_range__icontains=price_range)
    
    context = {
        'hotels': hotels,
        'query': query,
        'location': location,
        'hotel_type': hotel_type,
        'price_range': price_range,
        'user': request.user,
    }
    return render(request, 'hotel_service/hotel_list.html', context)

@login_required
def hotel_create(request):
    if request.method == 'POST':
        hotel = Hotel(
            name=request.POST.get('name'),
            hotel_type=request.POST.get('hotel_type'),
            address=request.POST.get('address'),
            location=request.POST.get('location'),
            city=request.POST.get('city', 'Delhi'),
            contact_number=request.POST.get('contact_number'),
            email=request.POST.get('email'),
            website=request.POST.get('website'),
            description=request.POST.get('description'),
            amenities=request.POST.get('amenities'),
            check_in_time=request.POST.get('check_in_time', '14:00'),
            check_out_time=request.POST.get('check_out_time', '12:00'),
            affiliate_link=request.POST.get('affiliate_link'),
            price_range=request.POST.get('price_range'),
            created_by=request.user
        )
        hotel.save()
        messages.success(request, 'Hotel added successfully! It will be visible after approval.')
        return redirect('hotel_service:hotel_list')
    return render(request, 'hotel_service/hotel_form.html')

def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk, is_approved=True)
    return render(request, 'hotel_service/hotel_detail.html', {'hotel': hotel})

@login_required
def hotel_edit(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.user != hotel.created_by and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this hotel.')
        return redirect('hotel_service:hotel_detail', pk=pk)
    
    if request.method == 'POST':
        hotel.name = request.POST.get('name')
        hotel.hotel_type = request.POST.get('hotel_type')
        hotel.address = request.POST.get('address')
        hotel.location = request.POST.get('location')
        hotel.city = request.POST.get('city', 'Delhi')
        hotel.contact_number = request.POST.get('contact_number')
        hotel.email = request.POST.get('email')
        hotel.website = request.POST.get('website')
        hotel.description = request.POST.get('description')
        hotel.amenities = request.POST.get('amenities')
        hotel.check_in_time = request.POST.get('check_in_time', '14:00')
        hotel.check_out_time = request.POST.get('check_out_time', '12:00')
        hotel.affiliate_link = request.POST.get('affiliate_link')
        hotel.price_range = request.POST.get('price_range')
        hotel.save()
        messages.success(request, 'Hotel updated successfully!')
        return redirect('hotel_service:hotel_detail', pk=pk)
    
    return render(request, 'hotel_service/hotel_form.html', {'hotel': hotel})

@login_required
def hotel_delete(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.user != hotel.created_by and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this hotel.')
        return redirect('hotel_service:hotel_detail', pk=pk)
    
    if request.method == 'POST':
        hotel.delete()
        messages.success(request, 'Hotel deleted successfully!')
        return redirect('hotel_service:hotel_list')
    
    return render(request, 'hotel_service/hotel_confirm_delete.html', {'hotel': hotel}) 