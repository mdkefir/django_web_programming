from django.contrib import admin

from cars.models import Brand, Car, Owner, Service, ServiceRecord

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'brand', 'year', 'color', 'user']
    list_filter = ['user']  # Фильтр по пользователю

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'car')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ('car', 'service', 'date', 'details')
# Register your models here.
