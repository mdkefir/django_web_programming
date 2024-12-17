"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from cars.api import CarsViewset, BrandViewSet, OwnerViewSet, ServiceViewSet, ServiceRecordViewSet
from cars.views import get_csrf_token, LoginView, ShowCarsView
from backend import views as backend_views

router = DefaultRouter()
router.register("cars", CarsViewset, basename="cars")
router.register("brands", BrandViewSet, basename="brands")
router.register('owners', OwnerViewSet, basename='owners')
router.register('services', ServiceViewSet, basename='services')
router.register('service-records', ServiceRecordViewSet, basename='service-records')

urlpatterns = [
    path('', ShowCarsView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path("admin/login/", LoginView.as_view(), name="login"),
    path('api/auth/csrf/', backend_views.get_csrf_token),
    path('api/auth/login/', backend_views.login_view),
    path('api/auth/logout/', backend_views.logout_view),
    path('api/auth/user/', backend_views.get_user),
    path('api/auth/otp-status/', backend_views.otp_status),
    path('api/auth/otp-qr-code/', backend_views.otp_qr_code),
    path('api/auth/otp-login/', backend_views.otp_login),
    path('api/geocode/', backend_views.geocode_address, name='geocode_address'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
