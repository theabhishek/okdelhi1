from django.db import models
from django.conf import settings
from django.utils import timezone

class LostAndFoundItem(models.Model):
    ITEM_TYPES = [
        ('LOST', 'Lost Item'),
        ('FOUND', 'Found Item'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('RESOLVED', 'Resolved'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date_lost_found = models.DateField()
    contact_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='lost_and_found/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_items')

    def __str__(self):
        return f"{self.get_item_type_display()}: {self.title}"

    class Meta:
        ordering = ['-created_at']
