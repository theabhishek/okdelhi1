from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Area, Landmark, FoodPlace, Market, Event, LandmarkReview, FoodPlaceReview, MarketReview, EventReview, MetroStation, MetroLine, MetroRoute
from .forms import AreaForm, LandmarkForm, FoodPlaceForm, MarketForm, EventForm, LandmarkReviewForm, FoodPlaceReviewForm, MarketReviewForm, EventReviewForm, SearchForm
from django.utils import timezone
from django.db.models import Q
from django.http import Http404
import requests
from decimal import Decimal
from django.conf import settings
import json
import os
from math import radians, sin, cos, sqrt, atan2

def area_list(request):
    areas = Area.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'delhi_wiki/area_list.html', {'areas': areas})

def area_detail(request, slug):
    area = get_object_or_404(Area, slug=slug)
    landmarks = Landmark.objects.filter(area=area)
    food_places = FoodPlace.objects.filter(area=area)
    markets = Market.objects.filter(area=area)
    events = Event.objects.filter(area=area)
    return render(request, 'delhi_wiki/area_detail.html', {
        'area': area,
        'landmarks': landmarks,
        'food_places': food_places,
        'markets': markets,
        'events': events,
    })

@login_required
def area_create(request):
    if request.method == 'POST':
        form = AreaForm(request.POST, request.FILES)
        if form.is_valid():
            area = form.save(commit=False)
            area.created_by = request.user
            area.save()
            messages.success(request, 'Area created successfully! It will be reviewed by our team.')
            return redirect('delhi_wiki:area_detail', slug=area.slug)
    else:
        form = AreaForm()
    return render(request, 'delhi_wiki/area_form.html', {'form': form})

@login_required
def area_approval_list(request):
    if not request.user.is_superuser:
        raise Http404
    areas = Area.objects.filter(is_approved=False).order_by('-created_at')
    return render(request, 'delhi_wiki/area_approval_list.html', {'areas': areas})

@login_required
def approve_area(request, slug):
    if not request.user.is_superuser:
        raise Http404
    area = get_object_or_404(Area, slug=slug)
    area.is_approved = True
    area.save()
    messages.success(request, f'Area "{area.name}" has been approved.')
    return redirect('delhi_wiki:area_approval_list')

def landmark_list(request):
    landmarks = Landmark.objects.filter(is_approved=True).order_by('name')
    return render(request, 'delhi_wiki/landmark_list.html', {'landmarks': landmarks})

@login_required
def landmark_approval_list(request):
    if not request.user.is_superuser:
        raise Http404
    landmarks = Landmark.objects.filter(is_approved=False).order_by('-created_at')
    return render(request, 'delhi_wiki/landmark_approval_list.html', {'landmarks': landmarks})

@login_required
def approve_landmark(request, slug):
    if not request.user.is_superuser:
        raise Http404
    landmark = get_object_or_404(Landmark, slug=slug)
    landmark.is_approved = True
    landmark.save()
    messages.success(request, f'Landmark "{landmark.name}" has been approved.')
    return redirect('delhi_wiki:landmark_approval_list')

def landmark_detail(request, slug):
    landmark = get_object_or_404(Landmark, slug=slug)
    reviews = LandmarkReview.objects.filter(landmark=landmark).order_by('-created_at')
    return render(request, 'delhi_wiki/landmark_detail.html', {
        'landmark': landmark,
        'reviews': reviews,
    })

@login_required
def landmark_create(request):
    if request.method == 'POST':
        form = LandmarkForm(request.POST, request.FILES)
        if form.is_valid():
            landmark = form.save(commit=False)
            landmark.created_by = request.user
            landmark.save()
            messages.success(request, 'Landmark created successfully! It will be reviewed by our team.')
            return redirect('delhi_wiki:landmark_detail', slug=landmark.slug)
    else:
        form = LandmarkForm()
    return render(request, 'delhi_wiki/landmark_form.html', {'form': form})

@login_required
def landmark_review_create(request, slug):
    landmark = get_object_or_404(Landmark, slug=slug)
    if request.method == 'POST':
        form = LandmarkReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.landmark = landmark
            review.author = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('delhi_wiki:landmark_detail', slug=landmark.slug)
    else:
        form = LandmarkReviewForm()
    return render(request, 'delhi_wiki/review_form.html', {
        'form': form,
        'title': f'Review {landmark.name}',
        'submit_text': 'Submit Review',
        'cancel_url': 'delhi_wiki:landmark_detail',
        'landmark': landmark
    })

def food_place_list(request):
    food_places = FoodPlace.objects.filter(is_approved=True).order_by('name')
    return render(request, 'delhi_wiki/food_place_list.html', {'food_places': food_places})

@login_required
def food_place_approval_list(request):
    if not request.user.is_superuser:
        raise Http404
    food_places = FoodPlace.objects.filter(is_approved=False).order_by('-created_at')
    return render(request, 'delhi_wiki/food_place_approval_list.html', {'food_places': food_places})

@login_required
def approve_food_place(request, slug):
    if not request.user.is_superuser:
        raise Http404
    food_place = get_object_or_404(FoodPlace, slug=slug)
    food_place.is_approved = True
    food_place.save()
    messages.success(request, f'Food Place "{food_place.name}" has been approved.')
    return redirect('delhi_wiki:food_place_approval_list')

def food_place_detail(request, slug):
    food_place = get_object_or_404(FoodPlace, slug=slug)
    reviews = FoodPlaceReview.objects.filter(food_place=food_place).order_by('-created_at')
    return render(request, 'delhi_wiki/food_place_detail.html', {
        'food_place': food_place,
        'reviews': reviews,
    })

@login_required
def food_place_create(request):
    if request.method == 'POST':
        form = FoodPlaceForm(request.POST, request.FILES)
        if form.is_valid():
            food_place = form.save(commit=False)
            food_place.created_by = request.user
            food_place.save()
            messages.success(request, 'Food place created successfully! It will be reviewed by our team.')
            return redirect('delhi_wiki:food_place_detail', slug=food_place.slug)
    else:
        form = FoodPlaceForm()
    return render(request, 'delhi_wiki/food_place_form.html', {'form': form})

@login_required
def food_place_review_create(request, slug):
    food_place = get_object_or_404(FoodPlace, slug=slug)
    if request.method == 'POST':
        form = FoodPlaceReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.food_place = food_place
            review.author = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('delhi_wiki:food_place_detail', slug=food_place.slug)
    else:
        form = FoodPlaceReviewForm()
    return render(request, 'delhi_wiki/review_form.html', {
        'form': form,
        'title': f'Review {food_place.name}',
        'submit_text': 'Submit Review',
        'cancel_url': 'delhi_wiki:food_place_detail',
        'food_place': food_place
    })

def market_list(request):
    markets = Market.objects.filter(is_approved=True).order_by('name')
    return render(request, 'delhi_wiki/market_list.html', {'markets': markets})

@login_required
def market_approval_list(request):
    if not request.user.is_superuser:
        raise Http404
    markets = Market.objects.filter(is_approved=False).order_by('-created_at')
    return render(request, 'delhi_wiki/market_approval_list.html', {'markets': markets})

@login_required
def approve_market(request, slug):
    if not request.user.is_superuser:
        raise Http404
    market = get_object_or_404(Market, slug=slug)
    market.is_approved = True
    market.save()
    messages.success(request, f'Market "{market.name}" has been approved.')
    return redirect('delhi_wiki:market_approval_list')

def market_detail(request, slug):
    market = get_object_or_404(Market, slug=slug)
    reviews = MarketReview.objects.filter(market=market).order_by('-created_at')
    return render(request, 'delhi_wiki/market_detail.html', {
        'market': market,
        'reviews': reviews,
    })

@login_required
def market_create(request):
    if request.method == 'POST':
        form = MarketForm(request.POST, request.FILES)
        if form.is_valid():
            market = form.save(commit=False)
            market.created_by = request.user
            market.save()
            messages.success(request, 'Market created successfully! It will be reviewed by our team.')
            return redirect('delhi_wiki:market_detail', slug=market.slug)
    else:
        form = MarketForm()
    return render(request, 'delhi_wiki/market_form.html', {'form': form})

@login_required
def market_review_create(request, slug):
    market = get_object_or_404(Market, slug=slug)
    if request.method == 'POST':
        form = MarketReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.market = market
            review.author = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('delhi_wiki:market_detail', slug=market.slug)
    else:
        form = MarketReviewForm()
    return render(request, 'delhi_wiki/review_form.html', {
        'form': form,
        'title': f'Review {market.name}',
        'submit_text': 'Submit Review',
        'cancel_url': 'delhi_wiki:market_detail',
        'market': market
    })

def event_list(request):
    events = Event.objects.filter(is_approved=True, end_date__gte=timezone.now()).order_by('start_date')
    return render(request, 'delhi_wiki/event_list.html', {'events': events})

@login_required
def event_approval_list(request):
    if not request.user.is_superuser:
        raise Http404
    events = Event.objects.filter(is_approved=False).order_by('-created_at')
    return render(request, 'delhi_wiki/event_approval_list.html', {'events': events})

@login_required
def approve_event(request, slug):
    if not request.user.is_superuser:
        raise Http404
    event = get_object_or_404(Event, slug=slug)
    event.is_approved = True
    event.save()
    messages.success(request, f'Event "{event.title}" has been approved.')
    return redirect('delhi_wiki:event_approval_list')

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'delhi_wiki/event_detail.html', {'event': event})

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, 'Event created successfully! It will be reviewed by our team.')
            return redirect('delhi_wiki:event_detail', slug=event.slug)
    else:
        form = EventForm()
    return render(request, 'delhi_wiki/event_form.html', {'form': form})

@login_required
def event_review_create(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        form = EventReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.event = event
            review.author = request.user
            review.created_at = timezone.now()
            review.save()
            messages.success(request, 'Your review has been added!')
            return redirect('delhi_wiki:event_detail', slug=event.slug)
    else:
        form = EventReviewForm()
    return render(request, 'delhi_wiki/review_form.html', {
        'form': form,
        'title': f'Review {event.title}',
        'submit_text': 'Submit Review',
        'cancel_url': 'delhi_wiki:event_detail',
        'event': event
    })

def search(request):
    query = request.GET.get('q', '')
    if query:
        # Search across all models
        areas = Area.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(location__icontains=query)
        ).filter(is_approved=True)
        
        landmarks = Landmark.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(address__icontains=query) |
            Q(category__icontains=query)
        ).filter(is_approved=True)
        
        food_places = FoodPlace.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(cuisine__icontains=query) |
            Q(area__name__icontains=query) |
            Q(address__icontains=query)
        ).filter(is_approved=True)
        
        markets = Market.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(specialties__icontains=query) |
            Q(area__name__icontains=query) |
            Q(address__icontains=query)
        ).filter(is_approved=True)
        
        events = Event.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(venue__icontains=query) |
            Q(area__name__icontains=query)
        ).filter(is_approved=True)
        
        context = {
            'query': query,
            'areas': areas,
            'landmarks': landmarks,
            'food_places': food_places,
            'markets': markets,
            'events': events,
            'has_results': any([areas.exists(), landmarks.exists(), food_places.exists(), markets.exists(), events.exists()])
        }
    else:
        context = {
            'query': '',
            'has_results': False
        }
    
    return render(request, 'delhi_wiki/search_results.html', context)

def metro_route_finder(request):
    # Get all stations and order them by name
    stations = MetroStation.objects.select_related().prefetch_related('lines').all().order_by('name')
    
    # Group stations by line for better organization
    lines = MetroLine.objects.prefetch_related('stations').all()
    stations_by_line = {}
    for line in lines:
        stations_by_line[line] = line.stations.all().order_by('name')
    
    context = {
        'stations': stations,
        'stations_by_line': stations_by_line,
        'lines': lines,
        'hide_nav': True
    }
    
    def get_route_data(source_station, destination_station):
        try:
            # First try static file
            json_file_path = os.path.join(settings.BASE_DIR, 'delhi_wiki', 'static', 'dmrc', 'metro_routes.json')
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        
        # If static file fails, use API
        try:
            api_url = "https://us-central1-delhimetroapi.cloudfunctions.net/route-get"
            api_key = os.getenv('DELHI_METRO_API_KEY', 'TGfInm24tkWHJxifYHU8v4lxU5O4aT0N')  # Fallback to default key
            
            params = {
                'from': source_station.name,
                'to': destination_station.name,
                'key': api_key
            }
            
            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    # Convert API response to our format
                    route_data = {
                        'routes': {
                            f"{source_station.name}-{destination_station.name}": {
                                'distance': float(data['data'].get('distance', 0)),
                                'fare': int(data['data'].get('fare', 0)),
                                'time': int(data['data'].get('time', 0)),
                                'interchange_stations': data['data'].get('interchange_stations', []),
                                'lines': [line.name for line in source_station.lines.all()] + [line.name for line in destination_station.lines.all()],
                                'intermediate_stations': data['data'].get('intermediate_stations', [])
                            }
                        },
                        'fares': {
                            '0-2': 10,
                            '2-5': 20,
                            '5-12': 30,
                            '12-21': 40,
                            '21-32': 50,
                            '32+': 60
                        }
                    }
                    return route_data
        except Exception:
            pass
        
        # If both methods fail, return basic fare structure
        return {
            'routes': {},
            'fares': {
                '0-2': 10,
                '2-5': 20,
                '5-12': 30,
                '12-21': 40,
                '21-32': 50,
                '32+': 60
            }
        }
    
    if request.method == 'POST':
        action = request.POST.get('action', '')
        
        if action == 'calculate_fare':
            source_id = request.POST.get('fare_source')
            destination_id = request.POST.get('fare_destination')
            
            if source_id and destination_id:
                try:
                    source = MetroStation.objects.get(id=source_id)
                    destination = MetroStation.objects.get(id=destination_id)
                    
                    # Get route data using the helper function
                    route_data = get_route_data(source, destination)
                    
                    # Try to find direct route
                    route_key = f"{source.name}-{destination.name}"
                    reverse_route_key = f"{destination.name}-{source.name}"
                    route_info = route_data['routes'].get(route_key) or route_data['routes'].get(reverse_route_key)
                    
                    if route_info:
                        distance = route_info['distance']
                        fare = route_info['fare']
                    else:
                        # Calculate direct distance
                        def calculate_distance(lat1, lon1, lat2, lon2):
                            R = 6371  # Earth's radius in kilometers
                            lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
                            dlat = lat2 - lat1
                            dlon = lon2 - lon1
                            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                            c = 2 * atan2(sqrt(a), sqrt(1-a))
                            distance = R * c
                            return distance
                        
                        distance = calculate_distance(
                            source.latitude, source.longitude,
                            destination.latitude, destination.longitude
                        )
                        
                        # Calculate fare based on distance
                        fare = 10  # base fare
                        for range_str, fare_amount in route_data['fares'].items():
                            if range_str == '32+':
                                if distance >= 32:
                                    fare = fare_amount
                                    break
                            else:
                                min_dist, max_dist = map(int, range_str.split('-'))
                                if min_dist <= distance <= max_dist:
                                    fare = fare_amount
                                    break
                    
                    context.update({
                        'fare_result': True,
                        'fare_source': source,
                        'fare_destination': destination,
                        'fare_distance': round(distance, 2),
                        'fare_amount': fare
                    })
                    
                except Exception as e:
                    context['error'] = f"Error calculating fare: {str(e)}"
        
        elif action == 'find_route':
            source_id = request.POST.get('source')
            destination_id = request.POST.get('destination')
            
            if source_id and destination_id:
                try:
                    source = MetroStation.objects.get(id=source_id)
                    destination = MetroStation.objects.get(id=destination_id)
                    
                    # Try to get existing route
                    route = MetroRoute.objects.filter(source=source, destination=destination).first()
                    
                    if not route:
                        # Get route data using the helper function
                        route_data = get_route_data(source, destination)

                        # Create route key (try both directions)
                        route_key = f"{source.name}-{destination.name}"
                        reverse_route_key = f"{destination.name}-{source.name}"
                        
                        # Get route info
                        route_info = route_data['routes'].get(route_key)
                        is_reverse = False
                        if not route_info:
                            route_info = route_data['routes'].get(reverse_route_key)
                            is_reverse = True
                        
                        if route_info:
                            # Create new route
                            route = MetroRoute.objects.create(
                                source=source,
                                destination=destination,
                                distance=route_info['distance'],
                                fare=route_info['fare'],
                                time=route_info['time']
                            )
                            
                            # Add interchange stations
                            for station_name in route_info.get('interchange_stations', []):
                                try:
                                    station = MetroStation.objects.get(name=station_name)
                                    route.interchange_stations.add(station)
                                except MetroStation.DoesNotExist:
                                    continue
                            
                            # Store intermediate stations in context
                            intermediate_stations = route_info.get('intermediate_stations', [])
                            if is_reverse:
                                intermediate_stations = list(reversed(intermediate_stations))
                            context['intermediate_stations'] = intermediate_stations
                            context['metro_lines'] = route_info['lines']
                        else:
                            # If direct route not found, calculate based on distance
                            def calculate_distance(lat1, lon1, lat2, lon2):
                                R = 6371  # Earth's radius in kilometers
                                lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
                                dlat = lat2 - lat1
                                dlon = lon2 - lon1
                                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                                c = 2 * atan2(sqrt(a), sqrt(1-a))
                                distance = R * c
                                return distance
                            
                            # Calculate direct distance
                            distance = calculate_distance(
                                source.latitude, source.longitude,
                                destination.latitude, destination.longitude
                            )
                            
                            # Calculate fare based on distance
                            fare = 10  # base fare
                            for range_str, fare_amount in route_data['fares'].items():
                                if range_str == '32+':
                                    if distance >= 32:
                                        fare = fare_amount
                                        break
                                else:
                                    min_dist, max_dist = map(int, range_str.split('-'))
                                    if min_dist <= distance <= max_dist:
                                        fare = fare_amount
                                        break
                            
                            # Estimate time (assuming average speed of 35 km/h)
                            estimated_time = round((distance / 35) * 60)  # Convert to minutes
                            
                            route = MetroRoute.objects.create(
                                source=source,
                                destination=destination,
                                distance=round(distance, 2),
                                fare=fare,
                                time=estimated_time
                            )
                            
                            # Check for potential interchange stations
                            common_lines = set(source.lines.all()) & set(destination.lines.all())
                            if not common_lines:
                                # Find potential interchange stations
                                interchange_stations = MetroStation.objects.filter(
                                    is_interchange=True,
                                    lines__in=source.lines.all()
                                ).filter(
                                    lines__in=destination.lines.all()
                                ).distinct()
                                
                                for station in interchange_stations:
                                    route.interchange_stations.add(station)
                                
                                context['metro_lines'] = [line.name for line in source.lines.all()] + \
                                                       [line.name for line in destination.lines.all()]
                    
                    if route:
                        context.update({
                            'route': route,
                            'source': source,
                            'destination': destination,
                        })
                        
                except Exception as e:
                    context['error'] = f"Error calculating route: {str(e)}"
    
    return render(request, 'delhi_wiki/metro_route_finder.html', context)

def metro_station_list(request):
    stations = MetroStation.objects.all()
    return render(request, 'delhi_wiki/metro_station_list.html', {'stations': stations})

def metro_station_detail(request, slug):
    station = get_object_or_404(MetroStation, slug=slug)
    return render(request, 'delhi_wiki/metro_station_detail.html', {'station': station})
