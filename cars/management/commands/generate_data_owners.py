from django.core.management.base import BaseCommand
from faker import Faker
from cars.models import Owner, Car

class Command(BaseCommand):
    help = "Генерация данных для владельцев"

    def handle(self, *args, **kwargs):
        fake = Faker(['ru_RU'])

        # Получение всех автомобилей из базы данных
        cars = list(Car.objects.all())
        if not cars:
            self.stdout.write(self.style.ERROR("Нет доступных автомобилей для назначения владельцев."))
            return

        def generate_russian_full_name():
            last_name = fake.last_name()
            first_name = fake.first_name()
            patronymic = fake.middle_name()
            return f"{last_name} {first_name} {patronymic}"
        
        # Генерация данных для владельцев
        for _ in range(996):  # Задайте нужное количество владельцев
            car = fake.random_element(cars)
            owner = Owner.objects.create(
                name=generate_russian_full_name(),
                car=car,
            )
            self.stdout.write(f"Создан владелец: {owner.name}, автомобиль: {car.brand.name} {car.name}")

        self.stdout.write(self.style.SUCCESS("Данные владельцев успешно сгенерированы!"))
