# Generated by Django 5.0.3 on 2024-03-29 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]