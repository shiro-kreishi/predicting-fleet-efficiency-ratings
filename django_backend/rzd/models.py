from django.conf import settings
from django.db import models
from django.utils import timezone


# Create your models here.


class Polygon(models.Model):
    name = models.TextField()
    short_name = models.TextField()
    polygon = models.TextField()


class Vehicle(models.Model):
    number = models.TextField()
    polygon = models.ForeignKey(Polygon, on_delete=models.CASCADE, related_name='vehicles')
    structural_unit = models.TextField()



class Fines(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fines')
    value = models.FloatField()



class Telematics(models.Model):
    date = models.TextField()  # Рассмотрите возможность использования models.DateField() если хотите хранить дату
    mileage = models.FloatField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='telematics')


class TripCard(models.Model):
    date = models.TextField()  # Аналогично, может быть models.DateField()
    mileage = models.FloatField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='trip_cards')


class DrivingStyle(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='driving_styles')
    value = models.TextField()
