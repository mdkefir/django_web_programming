from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    otp_key = models.CharField("OTP Key", max_length=32, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Генерируем OTP-ключ, если его нет
        if not self.otp_key:
            import pyotp
            self.otp_key = pyotp.random_base32()
        super().save(*args, **kwargs)

class Brand(models.Model):
    name = models.TextField("Название")

    class Meta:
        verbose_name = "Бренды"
        verbose_name_plural = "Бренд"

    def __str__(self) -> str:
        return self.name

class Car(models.Model):
    name = models.TextField("Модель")
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, verbose_name="Бренд", default=1)
    picture = models.ImageField("Изображение", null=True, upload_to="cars")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=True, blank=True)
    year = models.PositiveIntegerField("Год выпуска", null=True, blank=True)
    color = models.CharField("Цвет", max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self) -> str:
        return f"{self.brand.name} {self.name}"

class Owner(models.Model):
    name = models.CharField("Имя", max_length=255)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="owners", verbose_name="Автомобиль")

    class Meta:
        verbose_name = "Владелец"
        verbose_name_plural = "Владельцы"

    def __str__(self) -> str:
        return self.name

class Service(models.Model):
    name = models.CharField("Название сервиса", max_length=255)
    location = models.CharField("Местоположение", max_length=255)
    picture = models.ImageField("Изображение", null=True, upload_to="services")

    class Meta:
        verbose_name = "Сервис"
        verbose_name_plural = "Сервисы"

    def __str__(self) -> str:
        return self.name

class ServiceRecord(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="service_records", verbose_name="Автомобиль")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="service_records", verbose_name="Сервис")
    date = models.DateField("Дата обслуживания")
    details = models.TextField("Детали обслуживания", blank=True, null=True)

    class Meta:
        verbose_name = "Запись об обслуживании"
        verbose_name_plural = "Записи об обслуживании"

# Create your models here.
