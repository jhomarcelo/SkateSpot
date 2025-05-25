from django.contrib import admin
from django.urls import path,include
from skate_spots.views import SearchView, SearchAddressView
from rest_framework.routers import DefaultRouter
from skate_spots.views import SkateSpotViewSet, SkateShopViewSet, SkateEventViewSet, LocationViewSet, LocalImageViewSet, ModalityViewSet, StructureViewSet, CustomRegisterView
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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', SearchView.as_view(), name='search'),
    path('search_address/', SearchAddressView.as_view(), name='Busca Endereço'),
    path('', include(router.urls)),

    # Autenticação (login, logout, senha, token)
    path('api/auth/', include('dj_rest_auth.urls')),

    # Registro com verificação por e-mail
    path('api/auth/registration/', CustomRegisterView.as_view(), name='custom_register'),

    # Confirmação de e-mail (por django-allauth)
    path('api/auth/account/', include('allauth.account.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)