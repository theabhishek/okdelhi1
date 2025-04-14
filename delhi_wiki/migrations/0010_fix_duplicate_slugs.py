from django.db import migrations, models

def fix_duplicate_slugs(apps, schema_editor):
    MetroStation = apps.get_model('delhi_wiki', 'MetroStation')
    
    # Get all stations ordered by ID to ensure consistent ordering
    stations = MetroStation.objects.order_by('id')
    
    # Track seen slugs
    seen_slugs = {}
    
    # First pass: identify duplicates
    for station in stations:
        if station.slug in seen_slugs:
            seen_slugs[station.slug].append(station)
        else:
            seen_slugs[station.slug] = [station]
    
    # Second pass: fix duplicates
    for slug, stations in seen_slugs.items():
        if len(stations) > 1:
            # Keep the first station as is
            first_station = stations[0]
            
            # Update the rest
            for i, station in enumerate(stations[1:], 1):
                new_slug = f"{slug}-{i}"
                while MetroStation.objects.filter(slug=new_slug).exists():
                    i += 1
                    new_slug = f"{slug}-{i}"
                
                station.slug = new_slug
                station.save(update_fields=['slug'])

def reverse_fix(apps, schema_editor):
    # No need to reverse this migration
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('delhi_wiki', '0009_fix_duplicate_metro_stations'),
    ]

    operations = [
        # First, remove the unique constraint
        migrations.AlterField(
            model_name='metrostation',
            name='slug',
            field=models.SlugField(unique=False),
        ),
        # Run the fix function
        migrations.RunPython(fix_duplicate_slugs, reverse_fix),
        # Re-add the unique constraint
        migrations.AlterField(
            model_name='metrostation',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ] 