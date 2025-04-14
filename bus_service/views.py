from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F
from .models import Stop, Route, Trip, StopTime, FareRule, UserFareHistory, Agency
from .forms import RouteSearchForm, FareCalculationForm
from datetime import datetime, timedelta
from django.http import JsonResponse
import os
import csv
import random

def search_stops(request):
    query = request.GET.get('q', '').lower()
    stops = []
    
    try:
        # Read stops from the static file
        with open('busdata/stops.txt', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip header
            stop_code_idx = header.index('stop_code')
            stop_id_idx = header.index('stop_id')
            stop_name_idx = header.index('stop_name')
            zone_id_idx = header.index('zone_id')
            
            for row in reader:
                if len(row) >= 5:  # Ensure row has enough fields
                    stop_name = row[stop_name_idx].lower()
                    if query in stop_name:
                        stops.append({
                            'stop_id': row[stop_id_idx],
                            'stop_name': row[stop_name_idx],
                            'stop_code': row[stop_code_idx],
                            'zone_id': row[zone_id_idx]
                        })
                        if len(stops) >= 10:  # Limit to 10 results
                            break
    except Exception as e:
        print(f"Error reading stops: {e}")
    
    return JsonResponse({'stops': stops})

def get_realtime_vehicle_positions(route):
    """Generate static vehicle positions for demonstration"""
    vehicles = []
    try:
        # Read routes to get route information
        with open('busdata/routes.txt', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            route_id_idx = header.index('route_id')
            route_short_name_idx = header.index('route_short_name')
            
            # Find matching route
            for row in reader:
                if row[route_short_name_idx] == route.route_short_name:
                    # Generate 1-3 random vehicles for this route
                    num_vehicles = random.randint(1, 3)
                    for i in range(num_vehicles):
                        vehicles.append({
                            'label': f"{route.route_short_name}-{i+1}",
                            'current_status': random.choice(['IN_TRANSIT_TO', 'STOPPED_AT']),
                            'speed': random.randint(20, 40),
                            'timestamp': datetime.now() - timedelta(minutes=random.randint(1, 10))
                        })
                    break
    except Exception as e:
        print(f"Error generating vehicle positions: {e}")
    
    return vehicles

def route_search(request):
    if request.method == 'POST':
        form = RouteSearchForm(request.POST)
        if form.is_valid():
            origin_id = form.cleaned_data['origin_id']
            destination_id = form.cleaned_data['destination_id']
            
            # Get the stops
            origin = get_object_or_404(Stop, stop_id=origin_id)
            destination = get_object_or_404(Stop, stop_id=destination_id)
            
            # Find trips that go from origin to destination
            valid_trips = []
            trips = Trip.objects.filter(
                stop_times__stop=origin
            ).distinct()
            
            for trip in trips:
                # Get all stops for this trip in order
                stops_in_trip = StopTime.objects.filter(
                    trip=trip
                ).order_by('stop_sequence')
                
                # Check if destination comes after origin
                origin_found = False
                for stop_time in stops_in_trip:
                    if stop_time.stop == origin:
                        origin_found = True
                    elif origin_found and stop_time.stop == destination:
                        valid_trips.append(trip)
                        break
            
            # Get unique routes from valid trips
            routes = Route.objects.filter(
                trips__in=valid_trips
            ).distinct()
            
            # Add real-time vehicle positions to each route
            for route in routes:
                route.realtime_vehicles = get_realtime_vehicle_positions(route)
            
            if not routes.exists():
                messages.warning(request, 'No routes found between the selected stops.')
            
            return render(request, 'bus_service/route_search.html', {
                'form': form,
                'routes': routes,
                'origin': origin,
                'destination': destination
            })
    else:
        form = RouteSearchForm()
    
    return render(request, 'bus_service/route_search.html', {'form': form})

@login_required
def calculate_fare(request, route_id):
    route = get_object_or_404(Route, route_id=route_id)
    # Simplified fare calculation
    base_fare = 10
    fare = base_fare * (1 + (route.route_type / 10))  # Adjust fare based on route type
    return JsonResponse({'fare': round(fare, 2)})

@login_required
def fare_history(request):
    user_fares = UserFareHistory.objects.filter(user=request.user).order_by('-journey_date')
    return render(request, 'bus_service/fare_history.html', {
        'user_fares': user_fares
    })

def route_detail(request, route_id):
    route = get_object_or_404(Route, route_id=route_id)
    stops = Stop.objects.filter(
        stoptime__trip__route=route
    ).distinct().order_by('stoptime__stop_sequence')

    return render(request, 'bus_service/route_detail.html', {
        'route': route,
        'stops': stops
    })
