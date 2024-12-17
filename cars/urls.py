from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CarViewSet, BrandViewSet, OwnerViewSet, ServiceViewSet

router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'owners', OwnerViewSet)
router.register(r'services', ServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 