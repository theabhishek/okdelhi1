from django.db import migrations
from django.utils.text import slugify

def rebuild_metro_stations(apps, schema_editor):
    MetroStation = apps.get_model('delhi_wiki', 'MetroStation')
    MetroLine = apps.get_model('delhi_wiki', 'MetroLine')
    
    # First, remove all existing stations
    MetroStation.objects.all().delete()
    
    # Define all metro stations with their data
    stations_data = [
        # Yellow Line
        {'name': 'Samaypur Badli', 'lines': ['Yellow Line'], 'latitude': 28.7469, 'longitude': 77.1809},
        {'name': 'Rohini Sector 18, 19', 'lines': ['Yellow Line'], 'latitude': 28.7389, 'longitude': 77.1773},
        {'name': 'Haiderpur Badli Mor', 'lines': ['Yellow Line'], 'latitude': 28.7297, 'longitude': 77.1644},
        {'name': 'Jahangirpuri', 'lines': ['Yellow Line'], 'latitude': 28.7252, 'longitude': 77.1623},
        {'name': 'Adarsh Nagar', 'lines': ['Yellow Line'], 'latitude': 28.7171, 'longitude': 77.1690},
        {'name': 'Azadpur', 'lines': ['Yellow Line'], 'latitude': 28.7070, 'longitude': 77.1786},
        {'name': 'Model Town', 'lines': ['Yellow Line'], 'latitude': 28.7016, 'longitude': 77.1927},
        {'name': 'GTB Nagar', 'lines': ['Yellow Line'], 'latitude': 28.6972, 'longitude': 77.2067},
        {'name': 'Vishwa Vidyalaya', 'lines': ['Yellow Line'], 'latitude': 28.6881, 'longitude': 77.2139},
        {'name': 'Vidhan Sabha', 'lines': ['Yellow Line'], 'latitude': 28.6861, 'longitude': 77.2208},
        {'name': 'Civil Lines', 'lines': ['Yellow Line'], 'latitude': 28.6781, 'longitude': 77.2262},
        {'name': 'Kashmere Gate', 'lines': ['Yellow Line', 'Red Line', 'Violet Line'], 'latitude': 28.6675, 'longitude': 77.2288, 'is_interchange': True},
        {'name': 'Chandni Chowk', 'lines': ['Yellow Line'], 'latitude': 28.6586, 'longitude': 77.2302},
        {'name': 'Chawri Bazar', 'lines': ['Yellow Line'], 'latitude': 28.6492, 'longitude': 77.2282},
        {'name': 'New Delhi', 'lines': ['Yellow Line'], 'latitude': 28.6425, 'longitude': 77.2209},
        {'name': 'Rajiv Chowk', 'lines': ['Yellow Line', 'Blue Line'], 'latitude': 28.6333, 'longitude': 77.2182, 'is_interchange': True},
        {'name': 'Patel Chowk', 'lines': ['Yellow Line'], 'latitude': 28.6228, 'longitude': 77.2140},
        {'name': 'Central Secretariat', 'lines': ['Yellow Line', 'Violet Line'], 'latitude': 28.6147, 'longitude': 77.2116, 'is_interchange': True},
        {'name': 'Udyog Bhawan', 'lines': ['Yellow Line'], 'latitude': 28.6112, 'longitude': 77.2119},
        {'name': 'Lok Kalyan Marg', 'lines': ['Yellow Line'], 'latitude': 28.5977, 'longitude': 77.2107},
        {'name': 'Jor Bagh', 'lines': ['Yellow Line'], 'latitude': 28.5873, 'longitude': 77.2123},
        {'name': 'INA', 'lines': ['Yellow Line', 'Pink Line'], 'latitude': 28.5751, 'longitude': 77.2097, 'is_interchange': True},
        {'name': 'AIIMS', 'lines': ['Yellow Line'], 'latitude': 28.5684, 'longitude': 77.2074},
        {'name': 'Green Park', 'lines': ['Yellow Line'], 'latitude': 28.5598, 'longitude': 77.2066},
        {'name': 'Hauz Khas', 'lines': ['Yellow Line', 'Magenta Line'], 'latitude': 28.5432, 'longitude': 77.2065, 'is_interchange': True},
        {'name': 'Malviya Nagar', 'lines': ['Yellow Line'], 'latitude': 28.5297, 'longitude': 77.2062},
        {'name': 'Saket', 'lines': ['Yellow Line'], 'latitude': 28.5205, 'longitude': 77.2015},
        {'name': 'Qutab Minar', 'lines': ['Yellow Line'], 'latitude': 28.5138, 'longitude': 77.1870},
        {'name': 'Chhatarpur', 'lines': ['Yellow Line'], 'latitude': 28.5074, 'longitude': 77.1743},
        {'name': 'Sultanpur', 'lines': ['Yellow Line'], 'latitude': 28.5001, 'longitude': 77.1571},
        {'name': 'Ghitorni', 'lines': ['Yellow Line'], 'latitude': 28.4947, 'longitude': 77.1495},
        {'name': 'Arjan Garh', 'lines': ['Yellow Line'], 'latitude': 28.4808, 'longitude': 77.1262},
        {'name': 'Guru Dronacharya', 'lines': ['Yellow Line'], 'latitude': 28.4819, 'longitude': 77.1024},
        {'name': 'Sikandarpur', 'lines': ['Yellow Line'], 'latitude': 28.4800, 'longitude': 77.0919},
        {'name': 'MG Road', 'lines': ['Yellow Line'], 'latitude': 28.4795, 'longitude': 77.0765},
        {'name': 'IFFCO Chowk', 'lines': ['Yellow Line'], 'latitude': 28.4722, 'longitude': 77.0722},
        {'name': 'HUDA City Centre', 'lines': ['Yellow Line'], 'latitude': 28.4595, 'longitude': 77.0724},
    ]
    
    # Create metro lines first
    metro_lines = {}
    for line_name in ['Yellow Line', 'Red Line', 'Blue Line', 'Green Line', 'Violet Line', 'Pink Line', 'Magenta Line']:
        line, _ = MetroLine.objects.get_or_create(
            name=line_name,
            defaults={
                'color': '#FFFF00' if line_name == 'Yellow Line' else '#FF0000' if line_name == 'Red Line' else '#0000FF' if line_name == 'Blue Line' else '#008000' if line_name == 'Green Line' else '#800080' if line_name == 'Violet Line' else '#FFC0CB' if line_name == 'Pink Line' else '#FF00FF',
                'slug': slugify(line_name)
            }
        )
        metro_lines[line_name] = line
    
    # Create stations with unique slugs
    for station_data in stations_data:
        lines = station_data.pop('lines')
        station = MetroStation.objects.create(
            name=station_data['name'],
            slug=slugify(station_data['name']),
            latitude=station_data['latitude'],
            longitude=station_data['longitude'],
            is_interchange=station_data.get('is_interchange', False)
        )
        for line_name in lines:
            station.lines.add(metro_lines[line_name])

def reverse_rebuild(apps, schema_editor):
    # No need to reverse this migration
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('delhi_wiki', '0008_add_metro_stations'),
    ]

    operations = [
        migrations.RunPython(rebuild_metro_stations, reverse_rebuild),
    ] 