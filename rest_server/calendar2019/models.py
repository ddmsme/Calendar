from django.db import models

# Create your models here.
class Calendar2019(models.Model):
    date = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    nation = models.CharField(max_length=50)

