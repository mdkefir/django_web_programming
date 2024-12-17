# create_profiles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cars.models import UserProfile

class Command(BaseCommand):
    help = "Создание профилей для существующих пользователей"

    def handle(self, *args, **kwargs):
        users_without_profiles = User.objects.filter(profile__isnull=True)
        for user in users_without_profiles:
            UserProfile.objects.create(user=user)
            self.stdout.write(f"Профиль создан для пользователя: {user.username}")
