# Generated by Django 5.0.4 on 2024-06-23 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AddBussiness', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='country',
        ),
    ]
