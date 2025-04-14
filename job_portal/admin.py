from django.contrib import admin
from .models import Job, JobCategory, JobType, JobApplication, Notification

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'created_at')
    list_filter = ('job_type', 'created_at')
    search_fields = ('title', 'company', 'description')
    prepopulated_fields = {'slug': ('title', 'company')}
    readonly_fields = ('created_at', 'updated_at', 'views')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'company', 'location', 'description', 'requirements')
        }),
        ('Salary and Experience', {
            'fields': ('salary_min', 'salary_max', 'experience_min', 'experience_max')
        }),
        ('Job Details', {
            'fields': ('category', 'job_type', 'education', 'skills', 'benefits')
        }),
        ('Application Details', {
            'fields': ('application_deadline', 'contact_email', 'contact_phone', 'website')
        }),
        ('Status and Tracking', {
            'fields': ('status', 'is_filled', 'views', 'created_at', 'updated_at')
        }),
    )

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('job__title', 'applicant__username')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'job_application', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('recipient__username', 'message')
