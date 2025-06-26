from rest_framework.views import APIView
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import permissions
from geopy.distance import geodesic

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Avg, F
from .models import SkateSpot, SkateShop, SkateEvent, Location, LocalImage, Modality, Structure, CustomUser, Rating, validar_cep, consultar_cep
from .serializers import SkateSpotSerializer, SkateShopSerializer, SkateEventSerializer, LocationSerializer, LocalImageSerializer, ModalitySerializer, StructureSerializer, CustomRegisterSerializer, CustomUserDetailsSerializer, RatingSerializer, FavoriteActionSerializer
from dj_rest_auth.registration.views import RegisterView

from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateAPIView

#Retorna os locais
class SearchView(APIView):
    def get(self, request):
        user_latitude = float(request.query_params.get('lat', 0))
        user_longitude = float(request.query_params.get('lng', 0))
        search_query = request.query_params.get('query', '')
        filter_types = request.query_params.get('types', '').split(',')
        filter_modalities = request.query_params.get('modalidade', '').split(',')
        filter_structures = request.query_params.get('estrutura', '').split(',')

        results = []
        user_coords = (user_latitude, user_longitude)


        favorite_spot_ids = []
        if request.user.is_authenticated:
            favorite_spot_ids = list(request.user.favorite_spots.values_list('id', flat=True))


        #import pdb;pdb.set_trace()

        # Filtra pistas de skate
        if 'spots' in filter_types:
            spots = SkateSpot.objects.filter(location_id__latitude__isnull=False, location_id__longitude__isnull=False)
            if search_query:
                spots = spots.filter(name__icontains=search_query)

            if filter_modalities and filter_modalities != ['']:
                spots = spots.filter(modality__name__in=filter_modalities)

            if filter_structures and filter_structures != ['']:
                spots = spots.filter(structure__name__in=filter_structures)

            spots = spots.distinct()
        
            for spot in spots:
                location_coords = (spot.location_id.latitude, spot.location_id.longitude)
                distance = geodesic(user_coords, location_coords).km
                main_image = LocalImage.objects.filter(skatespot_id=spot, main_image=True).first()  # Obtém a imagem principal

                images_local = LocalImage.objects.filter(skatespot_id=spot)
                
                for image_local in images_local:
                    images.append({
                        'image': image_local.image.url
                    })
                
                # Verificar se é favorito
                is_favorite = spot.id in favorite_spot_ids
                



                results.append({
                    'id': spot.id,
                    'location_id': spot.location_id.id,
                    'name': spot.name,
                    'type': 'spot',
                    'latitude': spot.location_id.latitude,
                    'longitude': spot.location_id.longitude,
                    'main_image': main_image.image.url if main_image else '',  # Usa a imagem principal
                    'distance': distance,

                    'description': spot.description,
                    'images': images,
                    'is_favorite': is_favorite 

                    'description': spot.description

                })

        # Filtra skateshops
        if 'shops' in filter_types:
            shops = SkateShop.objects.filter(location_id__latitude__isnull=False, location_id__longitude__isnull=False)
            if search_query:
                shops = shops.filter(name__icontains=search_query)
            for shop in shops:
                location_coords = (shop.location_id.latitude, shop.location_id.longitude)
                distance = geodesic(user_coords, location_coords).km
                main_image = LocalImage.objects.filter(skateshop_id=shop, main_image=True).first()  # Obtém a imagem principal

                results.append({
                    'id': shop.id,
                    'location_id': shop.location_id.id,
                    'name': shop.name,
                    'type': 'shop',
                    'latitude': shop.location_id.latitude,
                    'longitude': shop.location_id.longitude,
                    'main_image': main_image.image.url if main_image else '',  # Usa a imagem principal
                    'distance': distance,
                    'description': shop.description
                })

        # Filtra eventos
        if 'events' in filter_types:
            events = SkateEvent.objects.filter(location_id__latitude__isnull=False, location_id__longitude__isnull=False)
            if search_query:
                events = events.filter(name__icontains=search_query)
            for event in events:
                location_coords = (event.location_id.latitude, event.location_id.longitude)
                distance = geodesic(user_coords, location_coords).km
                main_image = LocalImage.objects.filter(skateevent_id=event, main_image=True).first()  # Obtém a imagem principal
                
                results.append({
                    'id': event.id,
                    'location_id': event.location_id.id,
                    'name': event.name,
                    'type': 'event',
                    'latitude': event.location_id.latitude,
                    'longitude': event.location_id.longitude,
                    'main_image': main_image.image.url if main_image else '',  # Usa a imagem principal
                    'distance': distance,
                    'description': event.description
                })

        # Ordenando pela distância
        ordered_results = sorted(results, key=lambda x: x["distance"])

        return Response(ordered_results)


class SearchAddressView(APIView):
    def get(self, request):
        cep = request.query_params.get('cep', '')
        if cep:
            cep = cep.replace('-', '')  # Remove o hífen para a consulta
            data = consultar_cep(cep)
            if data:
                results = []
                results.append({
                    'cep': data.get('cep', ''),
                    'logradouro': data.get('address', ''),
                    'bairro': data.get('district', ''),
                    'cidade': data.get('city', ''),
                    'estado': data.get('state', ''),
                    'pais': 'Brasil' if data.get('state', '') else '',
                })
                return Response(results)


class SkateSpotViewSet(viewsets.ModelViewSet):
    queryset = SkateSpot.objects.annotate(
        avg_structures=Avg('rating__rating_structures'),
        avg_location=Avg('rating__rating_location'),
        avg_spot=Avg('rating__rating_spot'),
    )  
    serializer_class = SkateSpotSerializer


class SkateShopViewSet(viewsets.ModelViewSet):
    queryset = SkateShop.objects.all()
    serializer_class = SkateShopSerializer


class SkateEventViewSet(viewsets.ModelViewSet):
    queryset = SkateEvent.objects.all()
    serializer_class = SkateEventSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocalImageViewSet(viewsets.ModelViewSet):
    queryset = LocalImage.objects.all()
    serializer_class = LocalImageSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        skatespot_id = self.request.data.get("skatespot_id")
        skateshop_id = self.request.data.get("skateshop_id")
        skateevent_id = self.request.data.get("skateevent_id")

        is_main = False

        # Verifica se já existe imagem principal para o local
        if skatespot_id:
            exists = LocalImage.objects.filter(skatespot_id=skatespot_id, main_image=True).exists()
            if not exists:
                is_main = True

        elif skateshop_id:
            exists = LocalImage.objects.filter(skateshop_id=skateshop_id, main_image=True).exists()
            if not exists:
                is_main = True

        elif skateevent_id:
            exists = LocalImage.objects.filter(skateevent_id=skateevent_id, main_image=True).exists()
            if not exists:
                is_main = True

        serializer.save(user_id=self.request.user, main_image=is_main)

class ModalityViewSet(viewsets.ModelViewSet):
    queryset = Modality.objects.all()
    serializer_class = ModalitySerializer

class StructureViewSet(viewsets.ModelViewSet):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FavoriteActionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        spot_loc_id = serializer.validated_data['spot_id']
        action      = serializer.validated_data['action']

        try:
            spot = SkateSpot.objects.get(location_id=spot_loc_id)
        except SkateSpot.DoesNotExist:
            return Response({'error': 'Pista não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if action == 'favorite':
            user.favorite_spots.add(spot)
            return Response({'status': 'favoritado'}, status=status.HTTP_200_OK)

        user.favorite_spots.remove(spot)
        return Response({'status': 'desfavoritado'}, status=status.HTTP_200_OK)
    
class UserFavoritesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        favs = user.favorite_spots.select_related('location_id').all()

        data = []
        for spot in favs:
            data.append({
                'id':          spot.location_id.id,      
                'name':        spot.name,
                'type':        'spot',
                'latitude':    spot.location_id.latitude,
                'longitude':   spot.location_id.longitude,
                'main_image':  spot.localimage_set.filter(main_image=True).first().image.url if spot.localimage_set.filter(main_image=True).exists() else '',
                'distance':    0,                        
                'description': spot.description,
                'images':      [{'image': img.image.url} for img in spot.localimage_set.all()],
                'is_favorite': True,
            })

        return Response(data)

class CustomRegisterView(RegisterView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomRegisterSerializer


class CustomUserDetailsView(RetrieveUpdateAPIView):
    serializer_class = CustomUserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user