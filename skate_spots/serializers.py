# serializers.py
from rest_framework import serializers
from .models import SkateSpot, SkateShop, SkateEvent, Location, LocalImage, Modality, Structure, Rating
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class LocalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalImage
        fields = '__all__'


class SkateSpotSerializer(serializers.ModelSerializer):
    images = LocalImageSerializer(many=True, read_only=True)
    avg_structures = serializers.FloatField(read_only=True)
    avg_location   = serializers.FloatField(read_only=True)
    avg_spot       = serializers.FloatField(read_only=True)
    avg_overall    = serializers.SerializerMethodField()  

    class Meta:
        model = SkateSpot
        fields = [
            'id', 'name', 'description', 'lighting',
            'water', 'bathroom', 'create_date', 'location_id',
            'avg_structures', 'avg_location', 'avg_spot', 'avg_overall',
            'images',
        ]

    def get_avg_overall(self, obj):
        categories = [obj.avg_structures, obj.avg_location, obj.avg_spot]
        valid_categories = [v for v in categories if v is not None and v > 0]
        
        if not valid_categories:
            return 0
        
        return round(sum(valid_categories) / len(valid_categories), 2)



class SkateShopSerializer(serializers.ModelSerializer):
    images = LocalImageSerializer(many=True, read_only=True)
    class Meta:
        model = SkateShop
        fields = '__all__'


class SkateEventSerializer(serializers.ModelSerializer):
    images = LocalImageSerializer(many=True, read_only=True)
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
        read_only_fields = ('user',)
        
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


class RatingSerializer(serializers.ModelSerializer):
    skatespot = serializers.PrimaryKeyRelatedField(queryset=SkateSpot.objects.all())
    
    rating_structures = serializers.IntegerField(min_value=1, max_value=5)
    rating_location = serializers.IntegerField(min_value=1, max_value=5)
    rating_spot = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ['skatespot', 'rating_structures', 'rating_location', 'rating_spot']
        
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(required=False)
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES) 

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
        data['user_type'] = self.validated_data.get('user_type')
        return data

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            user.profile_picture = profile_picture
        user.user_type = self.cleaned_data.get('user_type')
        user.save()
        return user
    

class CustomUserDetailsSerializer(serializers.ModelSerializer):
    uploaded_images = LocalImageSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'profile_picture', 'user_type', 'uploaded_images')