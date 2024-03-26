# Generated by Django 5.0.3 on 2024-03-26 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_game_platform_profile_platforms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='genre',
        ),
        migrations.AddField(
            model_name='game',
            name='platforms',
            field=models.ManyToManyField(to='main_app.platform'),
        ),
        migrations.AddField(
            model_name='profile',
            name='games',
            field=models.ManyToManyField(to='main_app.game'),
        ),
    ]
