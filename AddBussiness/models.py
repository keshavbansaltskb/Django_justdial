from django.db import models
from Category.models import Category

class Business(models.Model):
    title = models.CharField(max_length=100)
    address = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    email = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=50)
    open_until = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    timing = models.CharField(max_length=100)
    service = models.TextField()
    overview = models.TextField()
    youtube = models.CharField(max_length=200, default='')
    image = models.ImageField(upload_to='business_images/')

class Search(models.Model):
    business_id = models.IntegerField() 
    city = models.CharField(max_length=100)

class Message(models.Model):
    business_id = models.IntegerField() 
    user =  models.CharField(max_length=200)
    email =  models.CharField(max_length=100)
    rating = models.IntegerField()
    message =  models.TextField()


class Gallery(models.Model):
    business_id = models.IntegerField()
    image = models.ImageField(upload_to='business_gallery/')

class Lead(models.Model):
    business_id = models.IntegerField() 
    user =  models.CharField(max_length=200)
    email =  models.CharField(max_length=100)
    search = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

class Adv(models.Model):
    business_email = models.CharField(max_length=100)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    image = models.ImageField(upload_to='advertisement_images/')
