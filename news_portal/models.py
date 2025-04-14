from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse

class News(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    CATEGORY_CHOICES = [
        ('POLITICS', 'Politics'),
        ('BUSINESS', 'Business'),
        ('TECHNOLOGY', 'Technology'),
        ('SPORTS', 'Sports'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('HEALTH', 'Health'),
        ('SCIENCE', 'Science'),
        ('WORLD', 'World'),
        ('LOCAL', 'Local'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news_articles')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    featured_image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_news')
    views = models.PositiveIntegerField(default=0)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "News"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            # If this is a new instance, use current time for the slug
            if not self.pk:
                self.slug = slugify(f"{self.title}-{timezone.now().strftime('%Y-%m-%d')}")
            else:
                self.slug = slugify(f"{self.title}-{self.created_at.strftime('%Y-%m-%d')}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news_portal:news_detail', kwargs={'slug': self.slug})

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

class NewsComment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.news.title}"
