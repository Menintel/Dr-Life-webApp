# Generated by Django 5.2 on 2025-05-09 10:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='next_available_appointment_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
