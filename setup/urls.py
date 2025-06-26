from django.contrib import admin
from django.urls import path,include
from skate_spots.views import SearchView, SearchAddressView
from rest_framework.routers import DefaultRouter
from skate_spots.views import SkateSpotViewSet, SkateShopViewSet, SkateEventViewSet, LocationViewSet, LocalImageViewSet, ModalityViewSet, StructureViewSet, CustomRegisterView, CustomUserDetailsView, RatingViewSet, FavoriteView, UserFavoritesView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'skate-spots', SkateSpotViewSet)
router.register(r'skate-shops', SkateShopViewSet)
router.register(r'skate-events', SkateEventViewSet)
router.register(r'location', LocationViewSet)
router.register(r'local-images', LocalImageViewSet)
router.register(r'modalities', ModalityViewSet)
router.register(r'structures', StructureViewSet)
router.register(r'ratings', RatingViewSet, basename='rating')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', SearchView.as_view(), name='search'),
    path('search_address/', SearchAddressView.as_view(), name='Busca Endereço'),
    path('', include(router.urls)),

    # Autenticação (login, logout, senha, token)
    path('api/auth/user/', CustomUserDetailsView.as_view(), name='custom_user_details'),
    
    # Registro com verificação por e-mail
    path('api/auth/registration/', CustomRegisterView.as_view(), name='custom_register'),
    
    # Confirmação de e-mail (por django-allauth)
    path('api/auth/account/', include('allauth.account.urls')),
<<<<<<< feat/favoritarpistas

    path('api/favorites/', FavoriteView.as_view(), name='favorites_action'),
    path('api/my-favorites/', UserFavoritesView.as_view(), name='user_favorites'),
=======
    
    path('api/auth/', include('dj_rest_auth.urls')),

>>>>>>> main
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)