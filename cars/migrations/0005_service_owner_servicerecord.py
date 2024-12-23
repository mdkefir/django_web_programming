# Generated by Django 5.1.1 on 2024-09-18 15:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0004_alter_brand_options_remove_car_brand_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название сервиса')),
                ('location', models.CharField(max_length=255, verbose_name='Местоположение')),
            ],
            options={
                'verbose_name': 'Сервис',
                'verbose_name_plural': 'Сервисы',
            },
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owners', to='cars.car')),
            ],
            options={
                'verbose_name': 'Владелец',
                'verbose_name_plural': 'Владельцы',
            },
        ),
        migrations.CreateModel(
            name='ServiceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата обслуживания')),
                ('details', models.TextField(blank=True, verbose_name='Детали обслуживания')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_records', to='cars.car')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_records', to='cars.service')),
            ],
            options={
                'verbose_name': 'Запись об обслуживании',
                'verbose_name_plural': 'Записи об обслуживании',
            },
        ),
    ]
