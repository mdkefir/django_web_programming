from rest_framework import serializers
from cars.models import User, Car, Brand, Owner, Service, ServiceRecord

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Выберите нужные поля

# Основной CarSerializer (brand как вложенный объект)
class CarDetailedSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()  # Вложенный сериализатор
    picture = serializers.ImageField(required=False)

    class Meta:
        model = Car
        fields = ['id', 'name', 'brand', 'picture', 'user', 'year', 'color']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
        #brand_data = validated_data.pop('brand')
        #brand, _ = Brand.objects.get_or_create(name=brand_data['name'])
        #validated_data['user'] = self.context['request'].user
        #car = Car.objects.create(brand=brand, **validated_data)
        #return car

    def update(self, instance, validated_data):
        brand_data = validated_data.pop('brand', None)
        if brand_data:
            brand, created = Brand.objects.get_or_create(name=brand_data['name'])
            instance.brand = brand
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.color = validated_data.get('color', instance.color)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.save()
        return instance

# Упрощенный CarSerializer (brand как ID)
class CarSimpleSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())  # brand как ID
    picture = serializers.ImageField(required=False)

    class Meta:
        model = Car
        fields = ['id', 'name', 'brand', 'picture', 'user', 'year', 'color']
        read_only_fields = ['user']  # Пользователь устанавливается автоматически

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.color = validated_data.get('color', instance.color)
        instance.year = validated_data.get('year', instance.year)
        instance.save()
        return instance

# Сериализатор с полной информацией об автомобиле
class OwnerDetailedSerializer(serializers.ModelSerializer):
    car = CarDetailedSerializer()  # Вложенный сериализатор для детализированного отображения

    class Meta:
        model = Owner
        fields = ['id', 'name', 'car']

# Сериализатор с использованием ID автомобиля
class OwnerSimpleSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())  # Используем ID для операций

    class Meta:
        model = Owner
        fields = ['id', 'name', 'car']

    def create(self, validated_data):
        # Создание владельца с использованием ID автомобиля
        owner = Owner.objects.create(**validated_data)
        return owner

    def update(self, instance, validated_data):
        # Обновление владельца
        instance.name = validated_data.get('name', instance.name)
        instance.car = validated_data.get('car', instance.car)
        instance.save()
        return instance

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class ServiceRecordDetailedSerializer(serializers.ModelSerializer):
    car = CarDetailedSerializer()  # Используем подробный сериализатор для автомобиля
    service = ServiceSerializer()  # Подробный сериализатор для сервиса

    class Meta:
        model = ServiceRecord
        fields = ['id', 'car', 'service', 'date', 'details']  # Все нужные поля



class ServiceRecordSimpleSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())  # Используем ID автомобиля
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())  # Используем ID сервиса

    class Meta:
        model = ServiceRecord
        fields = ['id', 'car', 'service', 'date', 'details']  # Поля для обработки

    def create(self, validated_data):
        # Создаем запись об обслуживании, связывая с автомобилем и сервисом по ID
        service_record = ServiceRecord.objects.create(**validated_data)
        return service_record

    def update(self, instance, validated_data):
        # Обновляем запись об обслуживании
        instance.car = validated_data.get('car', instance.car)
        instance.service = validated_data.get('service', instance.service)
        instance.date = validated_data.get('date', instance.date)
        instance.details = validated_data.get('details', instance.details)
        instance.save()
        return instance
