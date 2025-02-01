from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
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
    Consulta o CEP no ViaCEP e retorna os dados do endereço.
    """
    url = f'https://viacep.com.br/ws/{cep}/json/'
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


    def save(self, *args, **kwargs):
        """
        Preenche os campos de endereço com base no CEP antes de salvar.
        """
        self.full_clean()  # Valida o modelo
        cep = self.zip_code.replace('-', '')  # Remove o hífen para a consulta
        data = consultar_cep(cep)
        if data:
            self.street = data.get('logradouro', '')
            self.district = data.get('bairro', '')
            self.city = data.get('localidade', '')
            self.state = data.get('uf', '')
            
        super().save(*args, **kwargs)


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
    location_id = models.OneToOneField(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SkateShop(models.Model):

    name = models.CharField(verbose_name="Nome", max_length=30, blank=False)
    description = models.TextField(verbose_name="Descrição", max_length=250)
    location_id = models.OneToOneField(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class LocalImage(models.Model):

    image = models.ImageField(verbose_name="Imagem")
    main_image = models.BooleanField(verbose_name="Imagem Principal?", default=False)
    skatespot_id = models.ForeignKey(SkateSpot, null=True, blank=True, on_delete=models.CASCADE)
    skateshop_id = models.ForeignKey(SkateShop, null=True, blank=True, on_delete=models.CASCADE)
    skateevent_id = models.ForeignKey(SkateEvent, null=True, blank=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name="Data de Criação", auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.skatespot_id:
            self.image.field.upload_to = 'PISTAS/'  # Caminho para SkateSpot
        elif self.skateshop_id:
            self.image.field.upload_to = 'SKATESHOPS/'  # Caminho para SkateShop
        elif self.skateevent_id:
            self.image.field.upload_to = 'EVENTOS/'  # Caminho para SkateEvent
        super(LocalImage, self).save(*args, **kwargs)

    def __str__(self):
        return self.image.url  # Isso irá retornar o URL da imagem
    
