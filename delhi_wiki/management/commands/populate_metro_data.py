from django.core.management.base import BaseCommand
from delhi_wiki.models import MetroLine, MetroStation

class Command(BaseCommand):
    help = 'Populates the database with Delhi Metro lines and stations'

    def handle(self, *args, **kwargs):
        # Create Metro Lines
        lines = {
            'Red Line': '#E54B4B',
            'Yellow Line': '#F7D03C',
            'Blue Line': '#1E88E5',
            'Green Line': '#4CAF50',
            'Violet Line': '#9C27B0',
            'Orange Line': '#FF9800',
            'Magenta Line': '#E91E63',
            'Pink Line': '#FF69B4',
            'Grey Line': '#9E9E9E',
            'Rapid Metro': '#00BCD4',
        }

        metro_lines = {}
        for name, color in lines.items():
            line, created = MetroLine.objects.get_or_create(
                name=name,
                defaults={'color': color, 'description': f'Delhi Metro {name}'}
            )
            metro_lines[name] = line
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created {name}'))

        # Create Metro Stations
        stations_data = [
            # Yellow Line
            {
                'name': 'Samaypur Badli',
                'lines': ['Yellow Line'],
                'latitude': 28.7469,
                'longitude': 77.1809,
            },
            {
                'name': 'Rohini Sector 18, 19',
                'lines': ['Yellow Line'],
                'latitude': 28.7389,
                'longitude': 77.1773,
            },
            {
                'name': 'Haiderpur Badli Mor',
                'lines': ['Yellow Line'],
                'latitude': 28.7297,
                'longitude': 77.1644,
            },
            {
                'name': 'Jahangirpuri',
                'lines': ['Yellow Line'],
                'latitude': 28.7252,
                'longitude': 77.1623,
            },
            # Red Line
            {
                'name': 'Rithala',
                'lines': ['Red Line'],
                'latitude': 28.7219,
                'longitude': 77.1079,
            },
            {
                'name': 'Rohini West',
                'lines': ['Red Line'],
                'latitude': 28.7147,
                'longitude': 77.1118,
            },
            {
                'name': 'Rohini East',
                'lines': ['Red Line'],
                'latitude': 28.7134,
                'longitude': 77.1186,
            },
            # Blue Line
            {
                'name': 'Dwarka Sector 21',
                'lines': ['Blue Line'],
                'latitude': 28.5520,
                'longitude': 77.0587,
            },
            {
                'name': 'Dwarka Sector 8',
                'lines': ['Blue Line'],
                'latitude': 28.5657,
                'longitude': 77.0711,
            },
            {
                'name': 'Dwarka Sector 9',
                'lines': ['Blue Line'],
                'latitude': 28.5689,
                'longitude': 77.0644,
            },
            # Major Interchange Stations
            {
                'name': 'Rajiv Chowk',
                'lines': ['Yellow Line', 'Blue Line'],
                'latitude': 28.6333,
                'longitude': 77.2182,
                'is_interchange': True,
            },
            {
                'name': 'Kashmere Gate',
                'lines': ['Red Line', 'Yellow Line', 'Violet Line'],
                'latitude': 28.6675,
                'longitude': 77.2288,
                'is_interchange': True,
            },
            {
                'name': 'Central Secretariat',
                'lines': ['Yellow Line', 'Violet Line'],
                'latitude': 28.6147,
                'longitude': 77.2119,
                'is_interchange': True,
            },
            {
                'name': 'Mandi House',
                'lines': ['Blue Line', 'Violet Line'],
                'latitude': 28.6256,
                'longitude': 77.2343,
                'is_interchange': True,
            },
            {
                'name': 'Inderlok',
                'lines': ['Red Line', 'Green Line'],
                'latitude': 28.6728,
                'longitude': 77.1703,
                'is_interchange': True,
            },
        ]

        for station_data in stations_data:
            station_lines = station_data.pop('lines')
            station, created = MetroStation.objects.get_or_create(
                name=station_data['name'],
                defaults=station_data
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created station {station.name}'))
            
            # Add lines to station
            for line_name in station_lines:
                station.lines.add(metro_lines[line_name])

        self.stdout.write(self.style.SUCCESS('Successfully populated metro data')) 