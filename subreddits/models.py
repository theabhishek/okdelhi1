from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from users.models import CustomUser

class Subreddit(models.Model):
    APPROVAL_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500)
    rules = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_subreddits')
    moderators = models.ManyToManyField(CustomUser, related_name='moderated_subreddits', blank=True)
    subscribers = models.ManyToManyField(CustomUser, related_name='subscribed_subreddits', blank=True)
    banner = models.ImageField(upload_to='subreddit_banners/', null=True, blank=True)
    icon = models.ImageField(upload_to='subreddit_icons/', null=True, blank=True)
    approval_status = models.CharField(max_length=10, choices=APPROVAL_CHOICES, default='pending')
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_subreddits')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"r/{self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f"/r/{self.slug}/"
    
    def get_member_count(self):
        return self.subscribers.count()
    
    def is_approved(self):
        return self.approval_status == 'approved'
    
    def is_pending(self):
        return self.approval_status == 'pending'
    
    def is_rejected(self):
        return self.approval_status == 'rejected'
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Subreddit'
        verbose_name_plural = 'Subreddits' 