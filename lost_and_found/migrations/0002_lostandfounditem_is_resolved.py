# Generated by Django 5.0.1 on 2025-04-06 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lost_and_found', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lostandfounditem',
            name='is_resolved',
            field=models.BooleanField(default=False),
        ),
    ]
