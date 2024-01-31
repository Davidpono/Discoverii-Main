from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class User(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    program = models.CharField(max_length=255)
    weight = models.JSONField()
    bench = models.JSONField()
    squat = models.JSONField()
    deadlift = models.JSONField()
    custom = models.JSONField()
    meal = models.JSONField()

