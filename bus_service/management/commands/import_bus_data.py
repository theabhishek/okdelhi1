import os
import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from bus_service.models import Agency, Route, Stop, Trip, StopTime, FareAttribute, FareRule

class Command(BaseCommand):
    help = 'Import bus data from GTFS files'

    def handle(self, *args, **options):
        base_path = os.path.join(settings.BASE_DIR, 'busdata')
        
        # Import agency
        with open(os.path.join(base_path, 'agency.txt'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Agency.objects.get_or_create(
                    agency_id=row['agency_id'],
                    defaults={
                        'agency_name': row['agency_name'],
                        'agency_url': row['agency_url'],
                        'agency_timezone': row['agency_timezone']
                    }
                )

        # Import stops
        with open(os.path.join(base_path, 'stops.txt'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Stop.objects.get_or_create(
                    stop_id=row['stop_id'],
                    defaults={
                        'stop_code': row['stop_code'],
                        'stop_name': row['stop_name'],
                        'stop_lat': float(row['stop_lat']),
                        'stop_lon': float(row['stop_lon']),
                        'zone_id': row['zone_id']
                    }
                )

        # Import routes
        with open(os.path.join(base_path, 'routes.txt'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                agency = Agency.objects.get(agency_id=row['agency_id'])
                Route.objects.get_or_create(
                    route_id=row['route_id'],
                    defaults={
                        'agency': agency,
                        'route_short_name': row['route_short_name'],
                        'route_long_name': row['route_long_name'],
                        'route_type': int(row['route_type'])
                    }
                )

        # Import trips
        with open(os.path.join(base_path, 'trips.txt'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                route = Route.objects.get(route_id=row['route_id'])
                Trip.objects.get_or_create(
                    trip_id=row['trip_id'],
                    defaults={
                        'route': route,
                        'service_id': row['service_id'],
                        'shape_id': row.get('shape_id'),
                        'direction_id': 0,  # Default value
                        'wheelchair_accessible': 0,  # Default value
                        'bikes_allowed': 0  # Default value
                    }
                )

        # Import stop times
        with open(os.path.join(base_path, 'stop_times.txt'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                trip = Trip.objects.get(trip_id=row['trip_id'])
                stop = Stop.objects.get(stop_id=row['stop_id'])
                StopTime.objects.get_or_create(
                    trip=trip,
                    stop=stop,
                    stop_sequence=int(row['stop_sequence']),
                    defaults={
                        'arrival_time': row['arrival_time'],
                        'departure_time': row['departure_time'],
                        'pickup_type': int(row.get('pickup_type', 0)),
                        'drop_off_type': int(row.get('drop_off_type', 0))
                    }
                )

        # Import fare attributes
        with open(os.path.join(base_path, 'fare_attributes.txt'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                FareAttribute.objects.get_or_create(
                    fare_id=row['fare_id'],
                    defaults={
                        'price': float(row['price']),
                        'currency_type': row['currency_type'],
                        'payment_method': int(row['payment_method']),
                        'transfers': int(row['transfers'])
                    }
                )

        # Import fare rules
        with open(os.path.join(base_path, 'fare_rules.txt'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                fare = FareAttribute.objects.get(fare_id=row['fare_id'])
                route = Route.objects.get(route_id=row['route_id']) if row.get('route_id') else None
                FareRule.objects.get_or_create(
                    fare=fare,
                    route=route,
                    defaults={
                        'origin_id': row.get('origin_id'),
                        'destination_id': row.get('destination_id')
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported bus data')) 