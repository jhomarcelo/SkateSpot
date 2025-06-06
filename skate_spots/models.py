from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Avg
import requests
import re


def validar_cep(value):
    """
    Valida se o CEP está no formato correto.
    """
    if not re.match(r'^\d{5}-?\d{3}$', value):
        raise ValidationError('CEP inválido. O formato deve ser XXXXX-XXX.')


def consultar_cep(cep):
    """
    Consulta o CEP na AWESOMEAPI e retorna os dados do endereço.
    """
    #url = f'https://viacep.com.br/ws/{cep}/json/'
    url = f'https://cep.awesomeapi.com.br/json/{cep}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'erro' not in data:
            return data
    return None


class Location(models.Model):
    
    # TIPOS = [
    #     ('skatepark', 'Pista'),
    #     ('skateshop', 'Loja'),
    #    ('event', 'Evento')
    # ] 

    # type = models.CharField(verbose_name="Tipo", max_length=10, choices=TIPOS, blank=False)
    zip_code = models.CharField(verbose_name="CEP", max_length=9, blank=False, validators=[validar_cep])
    street = models.CharField(verbose_name="Logradouro", max_length=250, blank=False)
    number = models.CharField(verbose_name="Número", max_length=30, blank=False)
    district = models.CharField(verbose_name="Bairro", max_length=60, blank=False)
    city = models.CharField(verbose_name="Cidade", max_length=30, blank=False)
    state = models.CharField(verbose_name="Estado", max_length=30, blank=False)
    country = models.CharField(verbose_name="País", max_length=30, blank=False)
    latitude = models.FloatField(verbose_name="Latitude", blank=False)
    longitude = models.FloatField(verbose_name="Longitude", blank=False)


    # def save(self, *args, **kwargs):
    #     """
    #     Preenche os campos de endereço com base no CEP antes de salvar.
    #     """
    #     self.full_clean()  # Valida o modelo
    #     cep = self.zip_code.replace('-', '')  # Remove o hífen para a consulta
    #     data = consultar_cep(cep)
    #     if data:
    #         self.street = data.get('address', '')
    #         self.district = data.get('district', '')
    #         self.city = data.get('city', '')
    #         self.state = data.get('state', '')
            
    #     super().save(*args, **kwargs)


    def __str__(self):
        return self.zip_code
    

class SkateSpot(models.Model):

    name = models.CharField(verbose_name="Nome", max_length=30, blank=False)
    description = models.TextField(verbose_name="Descrição", max_length=250)
    lighting = models.BooleanField(verbose_name="Iluminacao Disponível?")
    water = models.BooleanField(verbose_name="Água Disponível?")
    bathroom = models.BooleanField(verbose_name="Banheiro Disponível?")
    create_date = models.DateTimeField(verbose_name="Data de Criação")
    location_id = models.OneToOneField(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SkateEvent(models.Model):

    name = models.CharField(verbose_name="Nome", max_length=30, blank=False)
    description = models.TextField(verbose_name="Descrição", max_length=250)
    start_date = models.DateTimeField(verbose_name="Data de Início", blank=False, default=timezone.now)
    end_date = models.DateTimeField(verbose_name="Data de Encerramento", blank=False, default=timezone.now)
    create_date = models.DateTimeField(verbose_name="Data de Criação", default=timezone.now)  
    location_id = models.OneToOneField(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SkateShop(models.Model):

    name = models.CharField(verbose_name="Nome", max_length=30, blank=False)
    description = models.TextField(verbose_name="Descrição", max_length=250)
    location_id = models.OneToOneField(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Modality(models.Model):
    name = models.CharField(verbose_name="Nome", max_length=30, blank=False)
    description = models.TextField(verbose_name="Descrição", max_length=250)
    create_date = models.DateTimeField(verbose_name="Data de Criação", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="Data de Atualização", auto_now=True)
    skatespot_id = models.ManyToManyField(SkateSpot, blank=True)

    def __str__(self):
        return self.name

class Structure(models.Model):
    name = models.CharField(verbose_name="Nome", max_length=30, blank=False)
    description = models.TextField(verbose_name="Descrição", max_length=250)
    skatespot_id = models.ManyToManyField(SkateSpot, blank=True)
    modality_id = models.ManyToManyField(Modality, blank=True)

    def __str__(self):
        return self.name

class Rating(models.Model):
    skatespot = models.ForeignKey(SkateSpot, on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    rating_structures = models.IntegerField(
        verbose_name="Nota estruturas",
        validators=[MinValueValidator(1), MaxValueValidator(5)] 
    )
    rating_location = models.IntegerField(
        verbose_name="Nota Localização",
        validators=[MinValueValidator(1), MaxValueValidator(5)]  
    )
    rating_spot = models.IntegerField(
        verbose_name="Nota Pista",
        validators=[MinValueValidator(1), MaxValueValidator(5)] 
    )
    create_date = models.DateTimeField(verbose_name="Data de Criação", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.skatespot.name}"

class LocalImage(models.Model):

    image = models.ImageField(verbose_name="Imagem")
    main_image = models.BooleanField(verbose_name="Imagem Principal?", default=False)
    skatespot_id = models.ForeignKey(SkateSpot, related_name='images', null=True, blank=True, on_delete=models.CASCADE)
    skateshop_id = models.ForeignKey(SkateShop, related_name='images', null=True, blank=True, on_delete=models.CASCADE)
    skateevent_id = models.ForeignKey(SkateEvent, related_name='images', null=True, blank=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name="Data de Criação", auto_now_add=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="uploaded_images")
    
    def save(self, *args, **kwargs):
        if self.skatespot_id:
            self.image.field.upload_to = 'PISTAS/'  # Caminho para SkateSpot
        elif self.skateshop_id:
            self.image.field.upload_to = 'SKATESHOPS/'  # Caminho para SkateShop
        elif self.skateevent_id:
            self.image.field.upload_to = 'EVENTOS/'  # Caminho para SkateEvent
        super(LocalImage, self).save(*args, **kwargs)

    def __str__(self):
        return self.id  # Isso irá retornar o URL da imagem


def user_profile_path(instance, filename):
    return f'users/profile_pics/{instance.username}/{filename}'

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('skater', 'Skater'),
        ('owner', 'Shop Owner'),
    )

    profile_picture = models.ImageField(upload_to=user_profile_path, blank=True, null=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='skater')

    def __str__(self):
        return self.username
