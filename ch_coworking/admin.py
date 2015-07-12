from django.contrib import admin

from .models import Amenity, Coworking, CoworkingPhoto, Table, Reservation

admin.site.register(Amenity)
admin.site.register(Coworking)
admin.site.register(CoworkingPhoto)
admin.site.register(Table)
admin.site.register(Reservation)
