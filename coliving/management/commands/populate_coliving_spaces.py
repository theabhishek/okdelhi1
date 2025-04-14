from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from coliving.models import ColivingSpace
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample coliving spaces'

    def handle(self, *args, **kwargs):
        # Create a superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        
        admin_user = User.objects.get(username='admin')

        # Sample coliving spaces data
        coliving_spaces = [
            {
                'title': 'Modern Co-living Hub',
                'description': 'A vibrant co-living space with modern amenities and a great community.',
                'property_type': 'Coliving',
                'gender_preference': 'Co-ed',
                'price_per_month': Decimal('15000.00'),
                'locality': 'Koramangala',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560034',
                'approval_status': 'Approved',
            },
            {
                'title': 'Tech Valley PG',
                'description': 'Premium PG accommodation near major tech parks with all facilities.',
                'property_type': 'PG',
                'gender_preference': 'Male',
                'price_per_month': Decimal('12000.00'),
                'locality': 'Electronic City',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560100',
                'approval_status': 'Approved',
            },
            {
                'title': 'Green View Hostel',
                'description': 'Peaceful hostel with garden views and excellent facilities.',
                'property_type': 'Hostel',
                'gender_preference': 'Female',
                'price_per_month': Decimal('10000.00'),
                'locality': 'Indiranagar',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560038',
                'approval_status': 'Approved',
            },
        ]

        # Create coliving spaces
        for space_data in coliving_spaces:
            space, created = ColivingSpace.objects.get_or_create(
                owner=admin_user,
                title=space_data['title'],
                defaults={
                    'description': space_data['description'],
                    'property_type': space_data['property_type'],
                    'gender_preference': space_data['gender_preference'],
                    'price_per_month': space_data['price_per_month'],
                    'locality': space_data['locality'],
                    'city': space_data['city'],
                    'state': space_data['state'],
                    'pincode': space_data['pincode'],
                    'approval_status': space_data['approval_status'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created coliving space: {space.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Coliving space already exists: {space.title}')) 