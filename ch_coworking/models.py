from django.conf import settings
from django.db import models

from model_utils.models import TimeStampedModel


class Amenity(models.Model):
    name = models.CharField(max_length=255)


class Coworking(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()
    opening = models.TimeField()
    closing = models.TimeField()

    amenities = models.ManyToManyField(Amenity, blank=True)


class Table(TimeStampedModel):
    name = models.CharField(max_length=255)
    coworking = models.ForeignKey(Coworking)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    notes = models.TextField()


class Reservation(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    table = models.ForeignKey(Table)
    date = models.DateField()
    from_hour = models.TimeField()
    to_hour = models.TimeField()
