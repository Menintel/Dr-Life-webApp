# Generated by Django 5.2 on 2025-05-28 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_alter_patient_dob'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='full_name',
        ),
    ]
