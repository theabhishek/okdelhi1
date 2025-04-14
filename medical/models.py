from django.db import models
from django.conf import settings
from django.utils import timezone

class MedicalFacility(models.Model):
    FACILITY_TYPES = [
        ('hospital', 'Hospital'),
        ('clinic', 'Clinic'),
        ('pharmacy', 'Pharmacy'),
        ('diagnostic', 'Diagnostic Center'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPES)
    address = models.TextField()
    location = models.CharField(max_length=200, help_text="Area/Locality")
    city = models.CharField(max_length=100, default="Delhi")
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    services = models.TextField(help_text="List of services provided")
    opening_hours = models.TextField(help_text="Opening hours and days")
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_facility_type_display()}"

    class Meta:
        verbose_name_plural = "Medical Facilities"
        ordering = ['-created_at']
