from rest_framework.views import APIView
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from geopy.distance import geodesic
from .models import SkateSpot, SkateShop, SkateEvent, Location, LocalImage, Modality, Structure, CustomUser, validar_cep, consultar_cep
from .serializers import SkateSpotSerializer, SkateShopSerializer, SkateEventSerializer, LocationSerializer, LocalImageSerializer, ModalitySerializer, StructureSerializer, FavoriteActionSerializer
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

#Retorna os locais
class SearchView(APIView):
    def get(self, request):
        user_latitude = float(request.query_params.get('lat', 0))
        user_longitude = float(request.query_params.get('lng', 0))
        search_query = request.query_params.get('query', '')
        filter_types = request.query_params.get('types', '').split(',')

        results = []
        user_coords = (user_latitude, user_longitude)

        favorite_spot_ids = []
        if request.user.is_authenticated:
            favorite_spot_ids = list(request.user.favorite_spots.values_list('id', flat=True))

        # Filtra pistas de skate
        if 'spots' in filter_types:
            spots = SkateSpot.objects.filter(location_id__latitude__isnull=False, location_id__longitude__isnull=False)
            if search_query:
                spots = spots.filter(name__icontains=search_query)
            for spot in spots:
                images = []
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
                    'id': spot.location_id.id,
                    'name': spot.name,
                    'type': 'spot',
                    'latitude': spot.location_id.latitude,
                    'longitude': spot.location_id.longitude,
                    'main_image': main_image.image.url if main_image else '',  # Usa a imagem principal
                    'distance': distance,
                    'description': spot.description,
                    'images': images,
                    'is_favorite': is_favorite 
                })

        # Filtra skateshops
        if 'shops' in filter_types:
            shops = SkateShop.objects.filter(location_id__latitude__isnull=False, location_id__longitude__isnull=False)
            if search_query:
                shops = shops.filter(name__icontains=search_query)
            for shop in shops:
                images = []
                location_coords = (shop.location_id.latitude, shop.location_id.longitude)
                distance = geodesic(user_coords, location_coords).km
                main_image = LocalImage.objects.filter(skateshop_id=shop, main_image=True).first()  # Obtém a imagem principal
                images_local = LocalImage.objects.filter(skateshop_id=shop)
                
                for image_local in images_local:
                    images.append({
                        'image': image_local.image.url
                    })

                results.append({
                    'id': shop.location_id.id,
                    'name': shop.name,
                    'type': 'shop',
                    'latitude': shop.location_id.latitude,
                    'longitude': shop.location_id.longitude,
                    'main_image': main_image.image.url if main_image else '',  # Usa a imagem principal
                    'distance': distance,
                    'description': shop.description,
                    'images': images
                })

        # Filtra eventos
        if 'events' in filter_types:
            events = SkateEvent.objects.filter(location_id__latitude__isnull=False, location_id__longitude__isnull=False)
            if search_query:
                events = events.filter(name__icontains=search_query)
            for event in events:
                images = []
                location_coords = (event.location_id.latitude, event.location_id.longitude)
                distance = geodesic(user_coords, location_coords).km
                main_image = LocalImage.objects.filter(skateevent_id=event, main_image=True).first()  # Obtém a imagem principal
                images_local = LocalImage.objects.filter(skateevent_id=event)
                
                for image_local in images_local:
                    images.append({
                        'image': image_local.image.url
                    })

                results.append({
                    'id': event.location_id.id,
                    'name': event.name,
                    'type': 'event',
                    'latitude': event.location_id.latitude,
                    'longitude': event.location_id.longitude,
                    'main_image': main_image.image.url if main_image else '',  # Usa a imagem principal
                    'distance': distance,
                    'description': event.description,
                    'images': images
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
                    'latitude': data.get('lat', ''),
                    'longitude': data.get('lng', ''),
                })
                return Response(results)


class SkateSpotViewSet(viewsets.ModelViewSet):
    queryset = SkateSpot.objects.all()
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

class ModalityViewSet(viewsets.ModelViewSet):
    queryset = Modality.objects.all()
    serializer_class = ModalitySerializer

class StructureViewSet(viewsets.ModelViewSet):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer


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