# Generated by Django 5.0.4 on 2024-06-28 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AddBussiness', '0023_alter_message_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='youtube',
            field=models.CharField(default='', max_length=200),
        ),
    ]
