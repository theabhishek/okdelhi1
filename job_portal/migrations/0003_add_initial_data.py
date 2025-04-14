from django.db import migrations
from django.utils.text import slugify

def add_initial_data(apps, schema_editor):
    JobCategory = apps.get_model('job_portal', 'JobCategory')
    JobType = apps.get_model('job_portal', 'JobType')

    # Add job categories
    categories = [
        'Information Technology',
        'Healthcare',
        'Finance',
        'Education',
        'Marketing',
        'Sales',
        'Customer Service',
        'Engineering',
        'Design',
        'Human Resources'
    ]

    for category in categories:
        JobCategory.objects.create(
            name=category,
            slug=slugify(category),
            description=f'Jobs in the {category} sector'
        )

    # Add job types
    job_types = [
        'Full-time',
        'Part-time',
        'Contract',
        'Internship',
        'Temporary',
        'Freelance',
        'Remote'
    ]

    for job_type in job_types:
        JobType.objects.create(
            name=job_type,
            slug=slugify(job_type),
            description=f'{job_type} employment opportunities'
        )

def remove_initial_data(apps, schema_editor):
    JobCategory = apps.get_model('job_portal', 'JobCategory')
    JobType = apps.get_model('job_portal', 'JobType')
    JobCategory.objects.all().delete()
    JobType.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('job_portal', '0002_alter_job_slug_alter_jobcategory_slug'),
    ]

    operations = [
        migrations.RunPython(add_initial_data, remove_initial_data),
    ] 