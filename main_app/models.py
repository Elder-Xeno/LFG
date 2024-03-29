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
    platforms = models.ManyToManyField(Platform)
    url = models.URLField()
    

    def __str__(self):
        return self.name

class Profile(models.Model):
    profile_image = models.ImageField(upload_to='profile_images', default='default-pic.JPG')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    games_owned = models.IntegerField(default=0)
    games = models.ManyToManyField(Game)
    platforms = models.ManyToManyField(Platform, blank=True)
    url = models.URLField()

    def __str__(self):
        return self.user.username
