from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class ColivingSpace(models.Model):
    PROPERTY_TYPES = [
        ('Coliving', 'Coliving Space'),
        ('PG', 'PG'),
        ('Hostel', 'Hostel'),
        ('Apartment', 'Apartment'),
        ('Independent House', 'Independent House'),
    ]

    GENDER_PREFERENCE = [
        ('Male', 'Male Only'),
        ('Female', 'Female Only'),
        ('Co-ed', 'Co-ed'),
    ]

    APPROVAL_STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='Coliving')
    gender_preference = models.CharField(max_length=10, choices=GENDER_PREFERENCE)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    approval_status = models.CharField(max_length=10, choices=APPROVAL_STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class ColivingImage(models.Model):
    coliving_space = models.ForeignKey(ColivingSpace, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='coliving_images/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.coliving_space.title}"

class Review(models.Model):
    coliving_space = models.ForeignKey(ColivingSpace, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coliving_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.coliving_space.title} by {self.user.username}"

    class Meta:
        unique_together = ['coliving_space', 'user']
