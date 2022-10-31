from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Company(models.Model):
    slug = models.SlugField(primary_key=True)

class Founder(models.Model):
    ph_username = models.CharField(max_length=255)

class TwitterInfo(models.Model):
    username = models.CharField(primary_key=True)
    founder = models.ForeignKey(Founder, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=255)
    scores = ArrayField(ArrayField(models.IntegerField()))

