from django.db import models
from django.conf import settings
from django.utils import timezone

class News(models.Model):
    CATEGORY_CHOICES = [
        ('TRAVEL', 'Travel'),
        ('TRANSPORT', 'Transport'),
        ('TECH', 'Technology'),
        ('BUSINESS', 'Business'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='OTHER')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views += 1
        self.save() 