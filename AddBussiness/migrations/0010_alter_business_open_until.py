# Generated by Django 5.0.4 on 2024-06-27 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AddBussiness', '0009_alter_message_business_id_alter_message_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='open_until',
            field=models.CharField(max_length=50),
        ),
    ]
