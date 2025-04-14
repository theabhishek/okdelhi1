from django.db import models
from django.conf import settings
from django.utils import timezone

class Hotel(models.Model):
    HOTEL_TYPES = [
        ('budget', 'Budget'),
        ('mid-range', 'Mid-Range'),
        ('luxury', 'Luxury'),
        ('boutique', 'Boutique'),
        ('resort', 'Resort'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    hotel_type = models.CharField(max_length=20, choices=HOTEL_TYPES)
    address = models.TextField()
    location = models.CharField(max_length=200, help_text="Area/Locality")
    city = models.CharField(max_length=100, default="Delhi")
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    amenities = models.TextField(help_text="List of amenities provided")
    check_in_time = models.TimeField(default='14:00')
    check_out_time = models.TimeField(default='12:00')
    affiliate_link = models.URLField(help_text="Booking affiliate link (e.g., OYO, Booking.com, etc.)")
    price_range = models.CharField(max_length=100, help_text="Price range per night (e.g., ₹1000-₹3000)")
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_hotel_type_display()}"

    class Meta:
        verbose_name_plural = "Hotels"
        ordering = ['-created_at'] 