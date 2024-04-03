from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django_resized import ResizedImageField


class Platform(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=100)
    platforms = models.ManyToManyField(Platform)
    url = models.URLField()
    cover_id = models.CharField(max_length=100)
    online_coop = models.BooleanField(default=False)
    genre = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name

class Profile(models.Model):
    profile_image = ResizedImageField(size=[200, 200], quality=75, upload_to="profile_images/", force_format='JPEG', blank=True, default='default-pic.JPG')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    games_owned = models.IntegerField(default=0)
    games = models.ManyToManyField(Game)
    platforms = models.ManyToManyField(Platform, blank=True)
    url = models.URLField()

    def __str__(self):
        return self.user.username
