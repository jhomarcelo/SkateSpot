# Generated by Django 4.2.18 on 2025-05-27 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skate_spots', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('skater', 'Skater'), ('owner', 'Shop Owner')], default='skater', max_length=10),
        ),
    ]
