from django.contrib import admin

from .models import Coworking, Table, Reservation

admin.site.register(Coworking)
admin.site.register(Table)
admin.site.register(Reservation)
