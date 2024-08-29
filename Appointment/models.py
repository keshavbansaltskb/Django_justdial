from django.db import models

# Create your models here.
class Appointment(models.Model):
    business_id = models.IntegerField() 
    user =  models.CharField(max_length=200)
    email =  models.CharField(max_length=100) 
    date = models.CharField(max_length=200)
    time = models.CharField(max_length=200)