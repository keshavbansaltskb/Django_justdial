# Generated by Django 5.0.4 on 2024-06-24 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AddBussiness', '0003_alter_business_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='email',
            field=models.CharField(default='', max_length=50),
        ),
    ]
