from django.db import models

class Category(models.Model):
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.category