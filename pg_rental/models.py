from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class PGListing(models.Model):
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

class PGImage(models.Model):
    pg_listing = models.ForeignKey(PGListing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='pg_images/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.pg_listing.title}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    pg_listing = models.ForeignKey(PGListing, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    mobile = models.CharField(max_length=15, default='')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Booking for {self.pg_listing.title} by {self.user.username}"

class Review(models.Model):
    pg_listing = models.ForeignKey(PGListing, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.pg_listing.title} by {self.user.username}"
