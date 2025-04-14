from django.core.management.base import BaseCommand
from pg_rental.models import PGListing
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates sample PG listings'
    
    def handle(self, *args, **kwargs):
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.ERROR('Please create a superuser first using python manage.py createsuperuser'))
            return
        
        admin = User.objects.filter(is_superuser=True).first()
        
        # Sample data for listing
        listings_data = [
            {
                'title': 'Modern Coliving Space Near Metro',
                'description': 'Well-furnished PG accommodation with all modern amenities. Located in a peaceful area with easy access to metro and market.',
                'property_type': 'Coliving',
                'gender_preference': 'Male',
                'price_per_month': 12000,
                'locality': 'Karol Bagh',
                'city': 'Delhi',
                'state': 'Delhi',
                'pincode': '110005',
            },
            {
                'title': 'Luxury PG for Working Professionals',
                'description': 'Spacious rooms with attached bathroom. Ideal for working professionals. All necessary facilities provided.',
                'property_type': 'PG',
                'gender_preference': 'Female',
                'price_per_month': 15000,
                'locality': 'Defence Colony',
                'city': 'Delhi',
                'state': 'Delhi',
                'pincode': '110024',
            },
            {
                'title': 'Budget Friendly Hostel',
                'description': 'Affordable PG with basic amenities. Located in a prime location with good connectivity.',
                'property_type': 'Hostel',
                'gender_preference': 'Co-ed',
                'price_per_month': 8000,
                'locality': 'Laxmi Nagar',
                'city': 'Delhi',
                'state': 'Delhi',
                'pincode': '110092',
            },
        ]
        
        for listing_data in listings_data:
            listing = PGListing(
                owner=admin,
                **listing_data
            )
            listing.save()
            
            self.stdout.write(self.style.SUCCESS(f'Created PG Listing: {listing.title}'))
            
        self.stdout.write(self.style.SUCCESS('Sample PG listings populated successfully!')) 