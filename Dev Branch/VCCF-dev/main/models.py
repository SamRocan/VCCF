from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
# django.db.models.JSONField
# Create your models here.


class Company(models.Model):
    slug = models.SlugField(primary_key=True)
    api = JSONField(default=dict, null=True)
    variables = JSONField(default=dict, null=True)
    twitterZip = JSONField(default=dict, null=True)
    websiteData = JSONField(default=dict, null=True)
    graphData = JSONField(default=dict, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.slug


class Founder(models.Model):
    ph_username = models.CharField(max_length=255, primary_key=True)
    company = models.ManyToManyField(Company)

    def __str__(self):
        return self.ph_username


class TwitterInfo(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    founder = models.ForeignKey(Founder, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=255)
    scores = ArrayField(ArrayField(models.IntegerField()))

    def __str__(self):
        return self.username

