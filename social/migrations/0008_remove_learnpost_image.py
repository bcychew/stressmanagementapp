# Generated by Django 3.0.3 on 2022-09-05 03:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_learnpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learnpost',
            name='image',
        ),
    ]
