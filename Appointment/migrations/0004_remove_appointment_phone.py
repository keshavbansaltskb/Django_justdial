# Generated by Django 5.0.4 on 2024-07-06 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment', '0003_alter_appointment_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='phone',
        ),
    ]
