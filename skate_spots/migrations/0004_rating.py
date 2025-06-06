# Generated by Django 4.2.18 on 2025-06-03 01:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skate_spots', '0003_alter_localimage_skateevent_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_structures', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Nota estruturas')),
                ('rating_location', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Nota Localização')),
                ('rating_spot', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Nota Pista')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('skatespot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skate_spots.skatespot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
