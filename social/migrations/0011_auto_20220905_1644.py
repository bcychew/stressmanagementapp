# Generated by Django 3.0.3 on 2022-09-05 08:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0010_remove_userprofile_friends'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learnpost',
            name='likes',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
    ]
