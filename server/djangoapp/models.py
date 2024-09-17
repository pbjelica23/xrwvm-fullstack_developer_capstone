from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    COUPE = 'Coupe'
    TRUCK = 'Truck'

    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (COUPE, 'Coupe'),
        (TRUCK, 'Truck'),
    ]

    car_make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE
    )
    dealer_id = models.IntegerField(
        blank=True,
        null=True
    )  # Allow blank and null values
    name = models.CharField(max_length=50)
    car_type = models.CharField(
        max_length=10,
        choices=CAR_TYPE_CHOICES,
        default=SEDAN
    )
    year = models.IntegerField(
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(2023)
        ]
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
