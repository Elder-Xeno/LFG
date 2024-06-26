# Generated by Django 5.0.3 on 2024-04-04 11:14

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_remove_profile_url_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='default-pic.JPG', force_format='JPEG', keep_meta=True, quality=75, scale=None, size=[200, 200], upload_to='profile_images/'),
        ),
    ]
