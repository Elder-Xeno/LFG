from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Platform(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name

class Profile(models.Model):
    games_owned = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    platforms = models.ManyToManyField(Platform, blank=True)

    def __str__(self):
        return self.user.username