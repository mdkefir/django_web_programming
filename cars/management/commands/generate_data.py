from django.core.management.base import BaseCommand
from faker import Faker
from cars.models import Car, Brand
import random

class Command(BaseCommand):
    help = "Генерация данных для автомобилей"

    def handle(self, *args, **kwargs):
        fake = Faker(['ru_RU'])

        # Предопределенные бренды и их серии
        brands_series_years = {
            "Audi": {
                "models": {
                    "A3": (1996, 2023),
                    "A4": (1994, 2023),
                    "A6": (1994, 2023),
                    "A8": (1994, 2023),
                    "Q7": (2005, 2023),
                    "Q5": (2008, 2023),
                    "TT": (1998, 2023),
                    "R8": (2006, 2023),
                }
            },
            "Hyundai": {
                "models": {
                    "Elantra": (1990, 2023),
                    "Sonata": (1985, 2023),
                    "Tucson": (2004, 2023),
                    "Santa Fe": (2000, 2023),
                    "Kona": (2017, 2023),
                }
            },
            "BMW": {
                "models": {
                    "M3": (1986, 2023),
                    "M4": (2014, 2023),
                    "M5": (1984, 2023),
                    "X5M": (2009, 2023),
                    "X6M": (2009, 2023),
                    "X3": (2003, 2023),
                    "X7": (2018, 2023),
                    "Z4": (2002, 2023),
                }
            },
            "Mitsubishi": {
                "models": {
                    "Lancer": (1973, 2017),
                    "Outlander": (2001, 2023),
                    "ASX": (2010, 2023),
                    "Pajero": (1982, 2023),
                    "Eclipse Cross": (2017, 2023),
                }
            },
            "Toyota": {
                "models": {
                    "Corolla": (1966, 2023),
                    "Camry": (1982, 2023),
                    "RAV4": (1994, 2023),
                    "Land Cruiser": (1951, 2023),
                    "Hilux": (1968, 2023),
                    "Prius": (1997, 2023),
                    "Supra": (1978, 2023),
                }
            },
            "Nissan": {
                "models": {
                    "Almera": (1995, 2018),
                    "X-Trail": (2000, 2023),
                    "Qashqai": (2006, 2023),
                    "Pathfinder": (1986, 2023),
                    "Leaf": (2010, 2023),
                    "Skyline": (1957, 2023),
                }
            },
            "Lada": {
                "models": {
                    "Vesta": (2015, 2023),
                    "Granta": (2011, 2023),
                    "Niva": (1977, 2023),
                    "XRAY": (2016, 2023),
                    "Kalina": (2004, 2018),
                }
            },
            "Volkswagen": {
                "models": {
                    "Golf": (1974, 2023),
                    "Passat": (1973, 2023),
                    "Tiguan": (2007, 2023),
                    "Touareg": (2002, 2023),
                    "Polo": (1975, 2023),
                    "Arteon": (2017, 2023),
                    "ID.4": (2020, 2023),
                }
            },
            "Tesla": {
                "models": {
                    "Model S": (2012, 2023),
                    "Model 3": (2017, 2023),
                    "Model X": (2015, 2023),
                    "Model Y": (2020, 2023),
                }
            },
            "Rolls-Royce": {
                "models": {
                    "Phantom": (1925, 2023),
                    "Ghost": (2009, 2023),
                    "Wraith": (2013, 2023),
                    "Cullinan": (2018, 2023),
                }
            },
            "Ford": {
                "models": {
                    "Focus": (1998, 2023),
                    "Explorer": (1990, 2023),
                    "Mustang": (1964, 2023),
                    "Ranger": (1983, 2023),
                    "Edge": (2006, 2023),
                }
            },
            "Chevrolet": {
                "models": {
                    "Tahoe": (1995, 2023),
                    "Camaro": (1966, 2023),
                    "Cruze": (2008, 2019),
                    "Equinox": (2004, 2023),
                    "Malibu": (1964, 2023),
                }
            },
            "Mercedes-Benz": {
                "models": {
                    "C-Class": (1993, 2023),
                    "E-Class": (1993, 2023),
                    "S-Class": (1972, 2023),
                    "GLE": (2015, 2023),
                    "GLS": (2016, 2023),
                }
            },
            "Ferrari": {
                "models": {
                    "488": (2015, 2023),
                    "Roma": (2020, 2023),
                    "F8": (2019, 2023),
                    "Portofino": (2017, 2023),
                    "SF90": (2019, 2023),
                }
            },
            "Opel": {
                "models": {
                    "Astra": (1991, 2023),
                    "Corsa": (1982, 2023),
                    "Insignia": (2008, 2023),
                    "Mokka": (2012, 2023),
                }
            },
            "Kia": {
                "models": {
                    "Rio": (2000, 2023),
                    "Sportage": (1993, 2023),
                    "Sorento": (2002, 2023),
                    "Ceed": (2006, 2023),
                    "K5": (2010, 2023),
                }
            },
            "Bentley": {
                "models": {
                    "Continental GT": (2003, 2023),
                    "Bentayga": (2016, 2023),
                    "Flying Spur": (2005, 2023),
                }
            },
            "Ferrari": {
                "models": {
                    "488": (2015, 2023),
                    "Roma": (2020, 2023),
                    "F8": (2019, 2023),
                    "Portofino": (2017, 2023),
                    "SF90": (2019, 2023),
                }
            },
            "Volvo": {
                "models": {
                    "XC90": (2002, 2023),
                    "XC60": (2008, 2023),
                    "XC40": (2017, 2023),
                    "S60": (2000, 2023),
                    "V90": (2016, 2023),
                }
            },
            "Rolls-Royce": {
                "models": {
                    "Phantom": (1925, 2023),
                    "Ghost": (2009, 2023),
                    "Wraith": (2013, 2023),
                    "Cullinan": (2018, 2023),
                }
            },
            "Renault": {
                "models": {
                    "Logan": (2004, 2023),
                    "Duster": (2010, 2023),
                    "Sandero": (2008, 2023),
                    "Kaptur": (2016, 2023),
                }
            },
            "Jaguar": {
                "models": {
                    "F-PACE": (2016, 2023),
                    "E-PACE": (2017, 2023),
                    "XF": (2007, 2023),
                    "XE": (2015, 2023),
                    "I-PACE": (2018, 2023),
                }
            },
            "Citroen": {
                "models": {
                    "C3": (2002, 2023),
                    "C4": (2004, 2023),
                    "C5 Aircross": (2017, 2023),
                }
            },
            "Bugatti": {
                "models": {
                    "Chiron": (2016, 2023),
                    "Veyron": (2005, 2015),
                    "Divo": (2018, 2021),
                }
            },
            "Maserati": {
                "models": {
                    "Ghibli": (2013, 2023),
                    "Levante": (2016, 2023),
                    "Quattroporte": (1963, 2023),
                    "MC20": (2020, 2023),
                }
            },
            "Cadillac": {
                "models": {
                    "Escalade": (1999, 2023),
                    "XT5": (2016, 2023),
                    "CT5": (2020, 2023),
                }
            },
            "Chevrolet": {
                "models": {
                    "Tahoe": (1995, 2023),
                    "Camaro": (1966, 2023),
                    "Cruze": (2008, 2019),
                    "Equinox": (2004, 2023),
                    "Malibu": (1964, 2023),
                }
            },
            "Subaru": {
                "models": {
                    "Forester": (1997, 2023),
                    "Outback": (1994, 2023),
                    "XV": (2011, 2023),
                    "Impreza": (1992, 2023),
                    "WRX": (2015, 2023),
                }
            },
            "Mazda": {
                "models": {
                    "CX-5": (2012, 2023),
                    "CX-9": (2006, 2023),
                    "Mazda3": (2003, 2023),
                    "Mazda6": (2002, 2023),
                    "MX-5": (1989, 2023),
                }
            },
            "Lexus": {
                "models": {
                    "RX": (1998, 2023),
                    "NX": (2014, 2023),
                    "GX": (2002, 2023),
                    "LX": (1996, 2023),
                    "IS": (1999, 2023),
                }
            },
            "Acura": {
                "models": {
                    "RDX": (2007, 2023),
                    "MDX": (2000, 2023),
                    "TLX": (2014, 2023),
                    "ILX": (2012, 2023),
                }
            },
            "Tesla": {
                "models": {
                    "Model S": (2012, 2023),
                    "Model 3": (2017, 2023),
                    "Model X": (2015, 2023),
                    "Model Y": (2020, 2023),
                }
            },
            "Dodge": {
                "models": {
                    "Charger": (1966, 2023),
                    "Challenger": (1970, 2023),
                    "Durango": (1998, 2023),
                    "RAM": (1981, 2023),
                }
            },
        }

        colors = ["Белый", "Чёрный", "Серый", "Красный", "Синий", "Коричневый", "Серебристый"]


        # Генерация брендов
        for brand_name in brands_series_years.keys():
            brand, created = Brand.objects.get_or_create(name=brand_name)
            if created:
                self.stdout.write(f"Создан бренд: {brand_name}")

        # Генерация автомобилей
        for _ in range(300):  # Количество генерируемых автомобилей
            brand_name = fake.random_element(list(brands_series_years.keys()))
            model_data = brands_series_years[brand_name]["models"]
            model_name, year_range = fake.random_element(list(model_data.items()))
            year = random.randint(*year_range)
            color = random.choice(colors)
            brand = Brand.objects.get(name=brand_name)

            car = Car.objects.create(
                name=model_name,
                brand=brand,
                year=year,
                color=color,
                user=None
            )
            self.stdout.write(f"Добавлен автомобиль: {brand_name} {model_name} ({year}), {color}")

        self.stdout.write(self.style.SUCCESS("Данные успешно сгенерированы!"))

