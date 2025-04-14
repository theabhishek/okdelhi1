from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from news.models import News
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populates the news database with sample data'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # Create a test user if none exists
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com', 'password': 'testpass123'}
        )
        
        # Sample news data
        news_data = [
            {
                'title': 'New Metro Line Opens in Delhi',
                'content': 'The new metro line connecting East Delhi to West Delhi has been inaugurated today. This will significantly reduce travel time for thousands of commuters.',
                'category': 'TRANSPORT',
            },
            {
                'title': 'Tech Startup Raises $10M in Funding',
                'content': 'A local tech startup has secured $10 million in Series A funding to expand its operations and develop new products.',
                'category': 'TECH',
            },
            {
                'title': 'Delhi Tourism Sees Record Numbers',
                'content': 'Delhi has seen a record number of tourists this season, with popular attractions like Red Fort and Qutub Minar seeing increased footfall.',
                'category': 'TRAVEL',
            },
            {
                'title': 'New Business District Planned',
                'content': 'The government has announced plans for a new business district in South Delhi, expected to create thousands of jobs.',
                'category': 'BUSINESS',
            },
            {
                'title': 'Local Festival Celebrates Culture',
                'content': 'The annual cultural festival brought together artists and performers from across the country to celebrate Delhi\'s rich heritage.',
                'category': 'OTHER',
            },
        ]
        
        # Create news articles
        for data in news_data:
            News.objects.create(
                title=data['title'],
                content=data['content'],
                author=user,
                category=data['category'],
                created_at=timezone.now(),
                is_published=True
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated news database')) 