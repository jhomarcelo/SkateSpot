# serializers.py
from rest_framework import serializers
from .models import SkateSpot, SkateShop, SkateEvent, Location, LocalImage, Modality, Structure
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class SkateSpotSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    
    class Meta:
        model = SkateSpot
        fields = '__all__'
    
    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited_by.filter(id=request.user.id).exists()
        return False


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

class FavoriteActionSerializer(serializers.Serializer):
    spot_id = serializers.IntegerField(required=True)
    action = serializers.ChoiceField(
        choices=['favorite', 'unfavorite'], 
        required=True
    )

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(required=False)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este e-mail já está em uso.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        return value

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        data['profile_picture'] = self.validated_data.get('profile_picture', None)
        return data

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            user.profile_picture = profile_picture
        user.save()
        return user