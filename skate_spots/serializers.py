# serializers.py
from rest_framework import serializers
from .models import SkateSpot, SkateShop, SkateEvent, Location, LocalImage, Modality, Structure


class SkateSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkateSpot
        fields = '__all__'  # Inclui todos os campos do modelo


class SkateShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkateShop
        fields = '__all__'


class SkateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkateEvent
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__' 


class LocalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalImage
        fields = '__all__' 

class ModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Modality
        fields = '__all__'

class StructureSerializer(serializers.ModelSerializer):
    skatespot_id = serializers.PrimaryKeyRelatedField(many=True, queryset=SkateSpot.objects.all())
    modality_id = serializers.PrimaryKeyRelatedField(many=True, queryset=Modality.objects.all())

    class Meta:
        model = Structure
        fields = '__all__'