from django.core.management.base import BaseCommand
from django.utils.text import slugify
from delhi_wiki.models import MetroStation, MetroLine

class Command(BaseCommand):
    help = 'Fixes duplicate metro station slugs'

    def handle(self, *args, **options):
        # Get all stations
        stations = MetroStation.objects.all()
        
        # Track seen slugs
        seen_slugs = {}
        
        # First pass: identify duplicates
        for station in stations:
            if station.slug in seen_slugs:
                seen_slugs[station.slug].append(station)
            else:
                seen_slugs[station.slug] = [station]
        
        # Second pass: fix duplicates
        for slug, duplicate_stations in seen_slugs.items():
            if len(duplicate_stations) > 1:
                self.stdout.write(f"Found {len(duplicate_stations)} stations with slug '{slug}'")
                
                # Keep the first station as is
                first_station = duplicate_stations[0]
                self.stdout.write(f"Keeping station '{first_station.name}' with slug '{first_station.slug}'")
                
                # Update the rest
                for i, station in enumerate(duplicate_stations[1:], 1):
                    new_slug = f"{slug}-{i}"
                    while MetroStation.objects.filter(slug=new_slug).exists():
                        i += 1
                        new_slug = f"{slug}-{i}"
                    
                    old_slug = station.slug
                    station.slug = new_slug
                    station.save()
                    self.stdout.write(f"Updated station '{station.name}' from '{old_slug}' to '{new_slug}'")
        
        self.stdout.write(self.style.SUCCESS('Successfully fixed duplicate metro station slugs')) 