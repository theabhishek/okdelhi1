from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = "Job Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class JobType(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Job(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CLOSED', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, null=True, blank=True)  # Non-unique for now
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='jobs')
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE, related_name='jobs')
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    is_filled = models.BooleanField(default=False)
    experience_min = models.PositiveIntegerField(null=True, blank=True)
    experience_max = models.PositiveIntegerField(null=True, blank=True)
    education = models.CharField(max_length=200, blank=True)
    skills = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    views = models.PositiveIntegerField(default=0)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_jobs')
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company}"

    def generate_unique_slug(self):
        """Generate a unique slug for the job."""
        base_slug = slugify(f"{self.title}-{self.company}")
        if not base_slug:
            base_slug = 'job'
        unique_slug = base_slug
        counter = 1
        while Job.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('job_portal:job_detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def close_job(self):
        self.status = 'CLOSED'
        self.save()

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHORTLISTED', 'Shortlisted'),
        ('REJECTED', 'Rejected'),
        ('HIRED', 'Hired'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
    cover_letter = models.TextField()
    resume_link = models.URLField(max_length=500, help_text="Link to your resume (Google Drive, Dropbox, etc.)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['job', 'applicant']

    def __str__(self):
        return f"{self.applicant.username}'s application for {self.job.title}"

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_notifications')
    job_application = models.ForeignKey('JobApplication', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.job_application.job.title}"

    class Meta:
        ordering = ['-created_at']
