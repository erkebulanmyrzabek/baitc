# Generated by Django 5.1.7 on 2025-03-14 11:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0003_remove_hackathon_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
