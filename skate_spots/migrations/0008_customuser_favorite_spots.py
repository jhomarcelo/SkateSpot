# Generated by Django 4.2.18 on 2025-06-26 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skate_spots', '0007_alter_location_latitude_alter_location_longitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='favorite_spots',
            field=models.ManyToManyField(blank=True, related_name='favorited_by', to='skate_spots.skatespot'),
        ),
    ]
