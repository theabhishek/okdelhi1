from django.db import models
from django.conf import settings
from django.utils import timezone

class Story(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    CATEGORY_CHOICES = [
        ('METRO', 'Metro Experience'),
        ('CAB', 'Cab Experience'),
        ('BUS', 'Bus Experience'),
        ('TRAIN', 'Train Experience'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='OTHER')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_stories')
    location = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='story_images/', null=True, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_stories', blank=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Stories'

    def __str__(self):
        return self.title

    def approve(self, admin_user):
        self.status = 'APPROVED'
        self.approved_at = timezone.now()
        self.approved_by = admin_user
        self.save()

    def reject(self, admin_user):
        self.status = 'REJECTED'
        self.approved_at = timezone.now()
        self.approved_by = admin_user
        self.save()
