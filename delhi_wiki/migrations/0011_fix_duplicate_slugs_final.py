from django.db import migrations
from django.utils.text import slugify

def fix_duplicate_slugs_final(apps, schema_editor):
    MetroStation = apps.get_model('delhi_wiki', 'MetroStation')
    MetroLine = apps.get_model('delhi_wiki', 'MetroLine')
    
    # First, backup all station data
    stations_data = []
    for station in MetroStation.objects.all():
        station_data = {
            'name': station.name,
            'slug': station.slug,
            'latitude': station.latitude,
            'longitude': station.longitude,
            'is_interchange': station.is_interchange,
            'lines': [line.name for line in station.lines.all()]
        }
        stations_data.append(station_data)
    
    # Delete all stations
    MetroStation.objects.all().delete()
    
    # Create metro lines lookup
    metro_lines = {line.name: line for line in MetroLine.objects.all()}
    
    # Recreate stations with unique slugs
    seen_slugs = set()
    for station_data in stations_data:
        base_slug = slugify(station_data['name'])
        slug = base_slug
        counter = 1
        
        # Ensure unique slug
        while slug in seen_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        seen_slugs.add(slug)
        
        # Create new station
        station = MetroStation.objects.create(
            name=station_data['name'],
            slug=slug,
            latitude=station_data['latitude'],
            longitude=station_data['longitude'],
            is_interchange=station_data['is_interchange']
        )
        
        # Add lines
        for line_name in station_data['lines']:
            if line_name in metro_lines:
                station.lines.add(metro_lines[line_name])

def reverse_fix(apps, schema_editor):
    # No need to reverse this migration
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('delhi_wiki', '0010_fix_duplicate_slugs'),
    ]

    operations = [
        migrations.RunPython(fix_duplicate_slugs_final, reverse_fix),
    ] 