# Generated by Django 5.0.3 on 2024-04-03 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_remove_game_cover_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='cover',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
