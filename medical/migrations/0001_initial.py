from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalFacility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('facility_type', models.CharField(choices=[('hospital', 'Hospital'), ('clinic', 'Clinic'), ('pharmacy', 'Pharmacy'), ('diagnostic', 'Diagnostic Center'), ('other', 'Other')], max_length=20)),
                ('address', models.TextField()),
                ('location', models.CharField(help_text='Area/Locality', max_length=200)),
                ('city', models.CharField(default='Delhi', max_length=100)),
                ('contact_number', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('website', models.URLField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('services', models.TextField(help_text='List of services provided')),
                ('opening_hours', models.TextField(help_text='Opening hours and days')),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Medical Facilities',
                'ordering': ['-created_at'],
            },
        ),
    ] 