from django.db import models

# Create your models here.
class Signup(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    phone = models.IntegerField()
    BUSINESS_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    bussiness = models.CharField(max_length=3, choices=BUSINESS_CHOICES, default='no')
    
class History(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)