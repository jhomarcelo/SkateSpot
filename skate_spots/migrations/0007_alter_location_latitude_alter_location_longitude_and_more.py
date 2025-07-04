# Generated by Django 4.2.18 on 2025-06-25 22:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skate_spots', '0006_modality_skatespot_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating_location',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Nota Localização'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating_spot',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Nota Pista'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating_structures',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Nota estruturas'),
        ),
    ]
