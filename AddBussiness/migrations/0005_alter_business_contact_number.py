# Generated by Django 5.0.4 on 2024-06-24 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AddBussiness', '0004_business_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='contact_number',
            field=models.CharField(max_length=50),
        ),
    ]
