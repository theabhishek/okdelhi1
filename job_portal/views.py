from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Job, JobApplication, JobCategory, Notification
from .forms import JobForm, JobApplicationForm
from django.utils import timezone

def is_superuser(user):
    return user.is_superuser

def job_list(request):
    try:
        jobs = Job.objects.filter(status='APPROVED', is_filled=False).order_by('-created_at')
        
        # Handle search
        query = request.GET.get('q')
        if query:
            jobs = jobs.filter(
                Q(title__icontains=query) |
                Q(company__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query) |
                Q(category__name__icontains=query)
            )
        
        # Handle category filter
        category_id = request.GET.get('category')
        if category_id:
            jobs = jobs.filter(category_id=category_id)
        
        # Handle job type filter
        job_type = request.GET.get('type')
        if job_type:
            jobs = jobs.filter(job_type=job_type)
        
        paginator = Paginator(jobs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        categories = JobCategory.objects.all()
        
        return render(request, 'job_portal/job_list.html', {
            'page_obj': page_obj,
            'categories': categories,
            'query': query,
            'selected_category': category_id,
            'selected_type': job_type
        })
    except Exception as e:
        # If there's an error with the database, return an empty job list
        return render(request, 'job_portal/job_list.html', {
            'page_obj': [],
            'categories': [],
            'query': None,
            'selected_category': None,
            'selected_type': None,
            'error_message': str(e)
        })

@login_required
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, 'Your job posting has been submitted for approval!')
            return redirect('job_portal:job_list')
    else:
        form = JobForm()
    return render(request, 'job_portal/create_job.html', {'form': form})

def job_detail(request, pk, slug):
    job = get_object_or_404(Job, pk=pk, slug=slug)
    if job.status != 'APPROVED' and not (request.user.is_superuser or request.user == job.posted_by):
        messages.error(request, 'This job posting is not available.')
        return redirect('job_portal:job_list')
    
    has_applied = False
    if request.user.is_authenticated:
        has_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
    
    return render(request, 'job_portal/job_detail.html', {
        'job': job,
        'has_applied': has_applied
    })

@login_required
def apply_job(request, pk, slug):
    job = get_object_or_404(Job, pk=pk, slug=slug)
    
    if job.status != 'APPROVED' or job.is_filled:
        messages.error(request, 'This job is not available for applications.')
        return redirect('job_portal:job_detail', pk=job.pk, slug=job.slug)
    
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_portal:job_detail', pk=job.pk, slug=job.slug)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('job_portal:job_detail', pk=job.pk, slug=job.slug)
    else:
        form = JobApplicationForm()
    
    return render(request, 'job_portal/apply_job.html', {
        'form': form,
        'job': job
    })

@login_required
@user_passes_test(is_superuser)
def pending_jobs(request):
    jobs = Job.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'job_portal/pending_jobs.html', {'jobs': jobs})

@login_required
@user_passes_test(is_superuser)
def approve_job(request, pk, slug):
    job = get_object_or_404(Job, pk=pk, slug=slug)
    job.status = 'APPROVED'
    job.approved_by = request.user
    job.approved_at = timezone.now()
    job.is_filled = False
    job.save()
    messages.success(request, f'Job "{job.title}" has been approved.')
    return redirect('job_portal:pending_jobs')

@login_required
@user_passes_test(is_superuser)
def reject_job(request, pk, slug):
    job = get_object_or_404(Job, pk=pk, slug=slug)
    job.status = 'REJECTED'
    job.approved_by = request.user
    job.approved_at = timezone.now()
    job.save()
    messages.success(request, f'Job "{job.title}" has been rejected.')
    return redirect('job_portal:pending_jobs')

@login_required
def my_jobs(request):
    jobs = Job.objects.filter(posted_by=request.user).order_by('-created_at')
    return render(request, 'job_portal/my_jobs.html', {'jobs': jobs})

@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(applicant=request.user).order_by('-created_at')
    return render(request, 'job_portal/my_applications.html', {
        'applications': applications
    })

@login_required
def close_job(request, pk, slug):
    job = get_object_or_404(Job, pk=pk, slug=slug)
    if request.user == job.posted_by or request.user.is_superuser:
        job.close_job()
        messages.success(request, f'Job "{job.title}" has been closed.')
    else:
        messages.error(request, 'You do not have permission to close this job.')
    return redirect('job_portal:job_detail', pk=pk, slug=slug)

@login_required
def job_applications(request, pk, slug):
    job = get_object_or_404(Job, pk=pk, slug=slug)
    
    # Check if user has permission to view applications
    if request.user != job.posted_by and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to view these applications.')
        return redirect('job_portal:job_detail', pk=job.pk, slug=job.slug)
    
    applications = job.applications.all().order_by('-created_at')
    
    return render(request, 'job_portal/job_applications.html', {
        'job': job,
        'applications': applications
    })

@login_required
def update_application_status(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    job = application.job
    
    if request.user != job.posted_by and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to update this application.')
        return redirect('job_portal:job_detail', pk=job.pk, slug=job.slug)
    
    status = request.POST.get('status')
    if status in ['PENDING', 'SHORTLISTED', 'REJECTED', 'HIRED']:
        application.status = status
        application.save()
        
        # Create notification for the applicant
        message = f"Your application for {job.title} has been {status.lower()}"
        Notification.objects.create(
            recipient=application.applicant,
            job_application=application,
            message=message
        )
        
        if status == 'HIRED':
            job.is_filled = True
            job.save()
            messages.success(request, f'Application has been marked as hired and the job has been closed.')
        else:
            messages.success(request, f'Application status has been updated to {application.get_status_display()}.')
    
    return redirect('job_portal:job_applications', pk=job.pk, slug=job.slug)

@login_required
def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    
    # Mark notifications as read when viewing
    notifications.update(is_read=True)
    
    return render(request, 'job_portal/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })
