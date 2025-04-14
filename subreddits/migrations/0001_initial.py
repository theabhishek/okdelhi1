from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subreddit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(max_length=500)),
                ('rules', models.TextField(blank=True, max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('banner', models.ImageField(blank=True, null=True, upload_to='subreddit_banners/')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='subreddit_icons/')),
                ('approval_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_subreddits', to=settings.AUTH_USER_MODEL)),
                ('moderators', models.ManyToManyField(blank=True, related_name='moderated_subreddits', to=settings.AUTH_USER_MODEL)),
                ('subscribers', models.ManyToManyField(blank=True, related_name='subscribed_subreddits', to=settings.AUTH_USER_MODEL)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_subreddits', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Subreddit',
                'verbose_name_plural': 'Subreddits',
                'ordering': ['-created_at'],
            },
        ),
    ] 