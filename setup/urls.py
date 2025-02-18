from django.contrib import admin
from django.urls import path,include
from skate_spots.views import SearchView, SearchAddressView
from rest_framework.routers import DefaultRouter
from skate_spots.views import SkateSpotViewSet, SkateShopViewSet, SkateEventViewSet, LocationViewSet, LocalImageViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'skate-spots', SkateSpotViewSet)
router.register(r'skate-shops', SkateShopViewSet)
router.register(r'skate-events', SkateEventViewSet)
router.register(r'location', LocationViewSet)
router.register(r'local-images', LocalImageViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', SearchView.as_view(), name='search'),
    path('search_address/', SearchAddressView.as_view(), name='Busca Endereço'),
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)