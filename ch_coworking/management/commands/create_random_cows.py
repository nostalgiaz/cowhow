from datetime import time

from django.contrib.auth import get_user_model
from django.core.management.base import NoArgsCommand
from django.utils.text import slugify

from geopy.geocoders import Nominatim

from ch_coworking.models import Coworking, Table


class Command(NoArgsCommand):
    def add_arguments(self, parser):
        parser.add_argument('places', nargs='+', type=str)

    def handle(self, *args, **options):
        geolocator = Nominatim()

        User = get_user_model()  # noqa

        for place in options.get('places'):
            location = geolocator.geocode(place)

            if not location:
                continue

            # create owner

            owner, created = User.objects.get_or_create(
                username='owner_{}'.format(slugify(place))
            )

            # create a coworker

            cow = Coworking.objects.create(
                owner=owner,
                name='Coworking in {}'.format(place),
                lat=location.latitude,
                lng=location.longitude,
                opening=time(10, 00),
                closing=time(20, 00),
            )

            for x in range(3):
                Table.objects.create(
                    name='Table {}'.format(x),
                    coworking=cow,
                    price=10.00
                )
