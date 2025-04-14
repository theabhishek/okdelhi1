from django.shortcuts import render
from delhi_wiki.models import MetroStation, MetroLine, MetroRoute
import json
from math import radians, sin, cos, sqrt, atan2

def metro_home(request):
    return render(request, 'metro/home.html')

def metro_route_finder(request):
    # Get all stations and order them by name
    stations = MetroStation.objects.all().order_by('name')
    
    # Get route data if stations are selected
    route_data = None
    if request.method == 'POST':
        source_station_id = request.POST.get('source_station')
        destination_station_id = request.POST.get('destination_station')
        
        if source_station_id and destination_station_id:
            source_station = MetroStation.objects.get(id=source_station_id)
            destination_station = MetroStation.objects.get(id=destination_station_id)
            
            # Get all possible routes between the stations
            routes = MetroRoute.objects.filter(
                stations=source_station
            ).filter(
                stations=destination_station
            ).distinct()
            
            if routes.exists():
                route = routes.first()
                route_data = {
                    'source': source_station.name,
                    'destination': destination_station.name,
                    'stations': [station.name for station in route.stations.all().order_by('order')],
                    'lines': [line.name for line in route.lines.all()],
                    'distance': route.distance,
                    'duration': route.duration
                }
    
    return render(request, 'metro/route_finder.html', {
        'stations': stations,
        'route_data': route_data
    })

def metro_station_list(request):
    stations = MetroStation.objects.all().order_by('name')
    return render(request, 'metro/station_list.html', {'stations': stations})

def metro_station_detail(request, slug):
    station = MetroStation.objects.get(slug=slug)
    return render(request, 'metro/station_detail.html', {'station': station}) 