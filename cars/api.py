from rest_framework.viewsets import GenericViewSet
from app.middleware import CsrfExemptSessionAuthentication
from rest_framework.authentication import BasicAuthentication
from cars.models import Car, Brand, Owner, Service, ServiceRecord
from rest_framework import mixins, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Min, Max
from cars.serializers import CarDetailedSerializer, CarSimpleSerializer, BrandSerializer, OwnerDetailedSerializer, OwnerSimpleSerializer, ServiceSerializer, ServiceRecordDetailedSerializer, ServiceRecordSimpleSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth import authenticate, login
from django.core.cache import cache
from django.http import HttpResponse
import pyotp
import qrcode
from io import BytesIO
from django.contrib.auth.models import User
from openpyxl import Workbook
from datetime import datetime

class CarsViewset(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Car.objects.all()
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CarSimpleSerializer  # Используем сериализатор с brand как ID
        return CarDetailedSerializer  # Используем детализированный сериализатор для GET-запросов
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        user = self.request.user
        queryset = Car.objects.all() if user.is_superuser else Car.objects.filter(user=user)

        # Фильтрация по параметрам
        name = self.request.query_params.get('name')
        brand = self.request.query_params.get('brand')
        year = self.request.query_params.get('year')
        color = self.request.query_params.get('color')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if brand:
            queryset = queryset.filter(brand_id=brand)
        if year:
            queryset = queryset.filter(year=year)
        if color:
            queryset = queryset.filter(color__icontains=color)

        return queryset
    
    class StatsSerializer(serializers.Serializer):
        total_cars = serializers.IntegerField()
        avg_year = serializers.FloatField()
        min_year = serializers.IntegerField()
        max_year = serializers.IntegerField()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        queryset = self.get_queryset()
        stats = queryset.aggregate(
            total_cars=Count('id'),
            avg_year=Avg('year'),
            min_year=Min('year'),
            max_year=Max('year'),
        )
        serializer = self.StatsSerializer(stats)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Экспорт данных в Excel"""
        # Создаем новый файл Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Автомобили"

        # Заголовки
        headers = ['ID', 'Название', 'Бренд', 'Год', 'Цвет']
        ws.append(headers)

        # Данные
        queryset = self.get_queryset()
        for car in queryset:
            ws.append([
                car.id,
                car.name,
                car.brand.name if car.brand else '',
                car.year,
                car.color
            ])

        # Автоматическая ширина колонок
        for column in ws.columns:
            max_length = 0
            column = list(column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column[0].column_letter].width = adjusted_width

        # Создаем HTTP-ответ
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=cars_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        # Сохраняем файл
        wb.save(response)
        return response

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        queryset = Brand.objects.all()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    class StatsSerializer(serializers.Serializer):
        total_brands = serializers.IntegerField()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        queryset = self.get_queryset()
        stats = queryset.aggregate(total_brands=Count('id'))
        serializer = self.StatsSerializer(stats)
        return Response(serializer.data)

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    def get_serializer_class(self):
        # Используем детализированный сериализатор для чтения, упрощённый для создания и обновления
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return OwnerSimpleSerializer
        return OwnerDetailedSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        queryset = Owner.objects.all()
        name = self.request.query_params.get('name')
        car_id = self.request.query_params.get('car')
        if name:
            queryset = queryset.filter(name__icontains=name)
        if car_id:
            queryset = queryset.filter(car_id=car_id)
        return queryset

    class StatsSerializer(serializers.Serializer):
        total_owners = serializers.IntegerField()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        queryset = self.get_queryset()
        stats = queryset.aggregate(total_owners=Count('id'))
        serializer = self.StatsSerializer(stats)
        return Response(serializer.data)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        queryset = Service.objects.all()
        name = self.request.query_params.get('name')
        location = self.request.query_params.get('location')
        if name:
            queryset = queryset.filter(name__icontains=name)
        if location:
            queryset = queryset.filter(location__icontains=location)
        return queryset

    class StatsSerializer(serializers.Serializer):
        total_services = serializers.IntegerField()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        queryset = self.get_queryset()
        stats = queryset.aggregate(total_services=Count('id'))
        serializer = self.StatsSerializer(stats)
        return Response(serializer.data)

class ServiceRecordViewSet(viewsets.ModelViewSet):
    queryset = ServiceRecord.objects.all()
    def get_serializer_class(self):
        # Используем детализированный сериализатор для чтения, упрощённый для создани и обновления
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return ServiceRecordSimpleSerializer
        return ServiceRecordDetailedSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    
    def get_queryset(self):
        queryset = ServiceRecord.objects.all()
        car_id = self.request.query_params.get('car')
        service_id = self.request.query_params.get('service')
        date = self.request.query_params.get('date')
        if car_id:
            queryset = queryset.filter(car_id=car_id)
        if service_id:
            queryset = queryset.filter(service_id=service_id)
        if date:
            queryset = queryset.filter(date=date)
        return queryset

    class StatsSerializer(serializers.Serializer):
        total_records = serializers.IntegerField()
        total_services = serializers.IntegerField()
        avg_records_per_service = serializers.FloatField()
        top_service_name = serializers.CharField()
        top_service_count = serializers.IntegerField()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        queryset = self.get_queryset()
        
        # Общая статистика
        total_records = queryset.count()
        total_services = queryset.values('service').distinct().count()
        
        # Среднее количество записей об обслуживании на сервис
        avg_records_per_service = (
            total_records / total_services if total_services > 0 else 0
        )

        # Сервис с максимальным количеством обслуживаний
        top_service = (
            queryset.values('service__name')
            .annotate(record_count=Count('id'))
            .order_by('-record_count')
            .first()
        )

        top_service_name = top_service['service__name'] if top_service else None
        top_service_count = top_service['record_count'] if top_service else 0

        # Собираем результат
        stats = {
            'total_records': total_records,
            'total_services': total_services,
            'avg_records_per_service': avg_records_per_service,
            'top_service_name': top_service_name,
            'top_service_count': top_service_count,
        }

        serializer = self.StatsSerializer(stats)
        return Response(serializer.data)
    
class SecuredModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Этот метод должен быть переопределен в дочерних классах
        raise NotImplementedError(
            "Необходимо определить get_queryset в %s" % self.__class__.__name__
        )

    class OTPSerializer(serializers.Serializer):
        key = serializers.CharField()

    class OTPRequired(BasePermission):
        """Проверка действующего OTP-токена"""
        def has_permission(self, request, view):
            return bool(cache.get(f'otp_good_{request.user.id}', False))

    @action(detail=False, methods=['POST'], url_path='otp-login', serializer_class=OTPSerializer)
    def otp_login(self, request, *args, **kwargs):
        totp = pyotp.TOTP(request.user.profile.otp_key)  # `otp_key` должен быть у пользователя
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success = False
        if totp.verify(serializer.validated_data['key']):
            cache.set(f'otp_good_{request.user.id}', True, timeout=300)  # Время жизни OTP (300 сек.)
            success = True

        return Response({'success': success}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='otp-status')
    def otp_status(self, request, *args, **kwargs):
        otp_good = cache.get(f'otp_good_{request.user.id}', False)
        return Response({'otp_good': otp_good}, status=status.HTTP_200_OK)

    def get_permissions(self):
        """Добавляем проверку на OTP для редактирования."""
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, self.OTPRequired]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'], url_path='otp-qr-code')
    def generate_qr_code(self, request, *args, **kwargs):
        # Убедитесь, что пользователь имеет профиль с OTP-ключом
        if not hasattr(request.user, 'profile') or not request.user.profile.otp_key:
            return Response({"error": "Профиль пользователя не настроен."}, status=400)

        # Создание OTP URI
        totp = pyotp.TOTP(request.user.profile.otp_key)
        otp_uri = totp.provisioning_uri(
            name=request.user.username,
            issuer_name="АвтоИнфо"
        )

        # Создание QR-кода
        qr = qrcode.make(otp_uri)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)

        # Возврат QR-кода в формате изображения
        return HttpResponse(buffer, content_type="image/png")