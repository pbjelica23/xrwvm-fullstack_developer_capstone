from django.core.management.base import BaseCommand
from djangoapp.models import CarMake, CarModel


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.initiate()

    def initiate(self):
        car_make_data = [
            {"name": "NISSAN", "description": "Japanese technology"},
            {"name": "Mercedes", "description": "German technology"},
            {"name": "Audi", "description": "German technology"},
            {"name": "Kia", "description": "Korean technology"},
            {"name": "Toyota", "description": "Japanese technology"},
        ]

        car_make_instances = []
        for data in car_make_data:
            car_make_instances.append(
                CarMake.objects.create(
                    name=data['name'],
                    description=data['description']
                )
            )

        car_model_data = [
            {"name": "Pathfinder", "car_type": "SUV", "year": 2023,
             "car_make": car_make_instances[0], "dealer_id": 1},
            {"name": "Qashqai", "car_type": "SUV", "year": 2023,
             "car_make": car_make_instances[0], "dealer_id": 1},
            {"name": "XTRAIL", "car_type": "SUV", "year": 2023,
             "car_make": car_make_instances[0], "dealer_id": 1},
            {"name": "A-Class", "car_type": "SUV", "year": 2023,
             "car_make": car_make_instances[1], "dealer_id": 2},
            {"name": "C-Class", "car_type": "SUV", "year": 2023,
             "car_make": car_make_instances[1], "dealer_id": 2},
            {"name": "E-Class", "car_type": "SUV", "year": 2023,
             "car_make": car_make_instances[1], "dealer_id": 2},
            {"name": "A4", "car_type": "SUV", "year": 2023,
             "car_make": car_make_instances[2], "dealer_id": 3},
            {"name": "A5", "car_type": "SUV", "year": 2023,
             "car_make": car_make_instances[2], "dealer_id": 3},
            {"name": "A6", "car_type": "SUV", "year": 2023,
             "car_make": car_make_instances[2], "dealer_id": 3},
            {"name": "Sorrento", "car_type": "SUV", "year": 2023,
             "car_make": car_make_instances[3], "dealer_id": 4},
            {"name": "Carnival", "car_type": "SUV", "year": 2023,
             "car_make": car_make_instances[3], "dealer_id": 4},
            {"name": "Cerato", "car_type": "Sedan", "year": 2023,
             "car_make": car_make_instances[3], "dealer_id": 4},
            {"name": "Corolla", "car_type": "Sedan", "year": 2023,
             "car_make": car_make_instances[4], "dealer_id": 5},
            {"name": "Camry", "car_type": "Sedan", "year": 2023,
             "car_make": car_make_instances[4], "dealer_id": 5},
            {"name": "Kluger", "car_type": "SUV", "year": 2023,
             "car_make": car_make_instances[4], "dealer_id": 5},
        ]

        for data in car_model_data:
            CarModel.objects.create(
                name=data['name'],
                car_make=data['car_make'],
                car_type=data['car_type'],
                year=data['year'],
                dealer_id=data['dealer_id']
            )
