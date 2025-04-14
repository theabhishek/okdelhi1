from django.db import models
from django.conf import settings
from django.utils import timezone

class Coupon(models.Model):
    STORE_CHOICES = [
        ('DOMINOS', 'Dominos'),
        ('AMAZON', 'Amazon'),
        ('FLIPKART', 'Flipkart'),
        ('ZOMATO', 'Zomato'),
        ('SWIGGY', 'Swiggy'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    store = models.CharField(max_length=20, choices=STORE_CHOICES)
    affiliate_link = models.URLField()
    discount_percentage = models.PositiveIntegerField(null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_coupons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='coupon_images/', null=True, blank=True)
    terms_and_conditions = models.TextField(blank=True)

    class Meta:
        app_label = 'coupon_service'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.store}"

    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_until

    def get_validity_status(self):
        now = timezone.now()
        if not self.is_active:
            return "Inactive"
        elif now < self.valid_from:
            return "Not Started"
        elif now > self.valid_until:
            return "Expired"
        else:
            return "Active"

class Click(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='clicks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    clicked_at = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        app_label = 'coupon_service'
        ordering = ['-clicked_at']

    def __str__(self):
        return f"Click on {self.coupon.title} by {self.user or 'Anonymous'}"
