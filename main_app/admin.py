from django.contrib import admin
from .models import Profile, Game, Platform

# Register your models here.
admin.site.register(Profile)
admin.site.register(Game)
admin.site.register(Platform)