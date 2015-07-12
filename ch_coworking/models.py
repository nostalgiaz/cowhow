from django.conf import settings
from django.db import models

from model_utils.models import TimeStampedModel


class CoworkingPhoto(TimeStampedModel):
    title = models.CharField('Title', max_length=100, blank=True)
    caption = models.TextField('Caption', blank=True)

    cover = models.BooleanField('Cover', default=False)

    photo = models.ImageField('Photo', upload_to='coworkings')

    class Meta:
        ordering = ['-cover']
        verbose_name = 'Coworking photo'
        verbose_name_plural = 'Coworking photos'


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
    photos = models.ManyToManyField(CoworkingPhoto, blank=True)

    def __unicode__(self):
        return self.name


class Table(TimeStampedModel):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    coworking = models.ForeignKey(Coworking, related_name='tables')
    price = models.DecimalField(decimal_places=2, max_digits=5)
    notes = models.TextField()

    def __unicode__(self):
        return self.name


class Reservation(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    table = models.ForeignKey(Table)
    date = models.DateField()
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    transaction_id = models.CharField(max_length=255)
