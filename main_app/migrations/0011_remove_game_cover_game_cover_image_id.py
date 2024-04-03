# Generated by Django 5.0.3 on 2024-04-03 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_game_cover'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='cover',
        ),
        migrations.AddField(
            model_name='game',
            name='cover_image_id',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]