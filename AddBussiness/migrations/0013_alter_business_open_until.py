# Generated by Django 5.0.4 on 2024-06-27 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AddBussiness', '0012_alter_business_open_until'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='open_until',
            field=models.CharField(default='', max_length=100),
        ),
    ]
