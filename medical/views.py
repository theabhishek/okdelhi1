from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import MedicalFacility

# Create your views here.

def medical_facility_list(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    facility_type = request.GET.get('type', '')
    
    facilities = MedicalFacility.objects.filter(is_approved=True)
    
    if query:
        facilities = facilities.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(services__icontains=query)
        )
    
    if location:
        facilities = facilities.filter(
            Q(location__icontains=location) |
            Q(city__icontains=location)
        )
    
    if facility_type:
        facilities = facilities.filter(facility_type=facility_type)
    
    context = {
        'facilities': facilities,
        'query': query,
        'location': location,
        'facility_type': facility_type,
    }
    return render(request, 'medical/facility_list.html', context)

@login_required
def medical_facility_create(request):
    if request.method == 'POST':
        facility = MedicalFacility(
            name=request.POST.get('name'),
            facility_type=request.POST.get('facility_type'),
            address=request.POST.get('address'),
            location=request.POST.get('location'),
            city=request.POST.get('city', 'Delhi'),
            contact_number=request.POST.get('contact_number'),
            email=request.POST.get('email'),
            website=request.POST.get('website'),
            description=request.POST.get('description'),
            services=request.POST.get('services'),
            opening_hours=request.POST.get('opening_hours'),
            created_by=request.user
        )
        facility.save()
        messages.success(request, 'Medical facility added successfully! It will be visible after approval.')
        return redirect('medical:facility_list')
    return render(request, 'medical/facility_form.html')

def medical_facility_detail(request, pk):
    facility = get_object_or_404(MedicalFacility, pk=pk)
    return render(request, 'medical/facility_detail.html', {'facility': facility})

@login_required
def medical_facility_edit(request, pk):
    facility = get_object_or_404(MedicalFacility, pk=pk)
    if request.user != facility.created_by and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this facility.')
        return redirect('medical:facility_detail', pk=pk)
    
    if request.method == 'POST':
        facility.name = request.POST.get('name')
        facility.facility_type = request.POST.get('facility_type')
        facility.address = request.POST.get('address')
        facility.location = request.POST.get('location')
        facility.city = request.POST.get('city', 'Delhi')
        facility.contact_number = request.POST.get('contact_number')
        facility.email = request.POST.get('email')
        facility.website = request.POST.get('website')
        facility.description = request.POST.get('description')
        facility.services = request.POST.get('services')
        facility.opening_hours = request.POST.get('opening_hours')
        facility.save()
        messages.success(request, 'Medical facility updated successfully!')
        return redirect('medical:facility_detail', pk=pk)
    
    return render(request, 'medical/facility_form.html', {'facility': facility})

@login_required
def medical_facility_delete(request, pk):
    facility = get_object_or_404(MedicalFacility, pk=pk)
    if request.user != facility.created_by and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this facility.')
        return redirect('medical:facility_detail', pk=pk)
    
    if request.method == 'POST':
        facility.delete()
        messages.success(request, 'Medical facility deleted successfully!')
        return redirect('medical:facility_list')
    
    return render(request, 'medical/facility_confirm_delete.html', {'facility': facility})
