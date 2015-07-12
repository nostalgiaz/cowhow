from datetime import time

from django.contrib.auth import get_user_model
from django.core.management.base import NoArgsCommand
from django.utils.text import slugify

from geopy.geocoders import Nominatim

from ch_coworking.models import Coworking, Table
from ch_users.serializers import MerchantAccountSerializer


class Command(NoArgsCommand):
    def add_arguments(self, parser):
        parser.add_argument('places', nargs='+', type=str)

    def create_merchant(self, user):
        serializer = MerchantAccountSerializer(data={
            'individual': {
                'first_name': "Jane",
                'last_name': "Doe",
                'email': "jane@14ladders.com",
                'phone': "5553334444",
                'date_of_birth': "1981-11-19",
                'ssn': "456-45-4567",
                'address': {
                    'street_address': "111 Main St",
                    'locality': "Chicago",
                    'region': "IL",
                    'postal_code': "60622"
                }
            },
            'funding': {
                'descriptor': "Blue Ladders",
                'email': "funding@blueladders.com",
                'mobile_phone': "5555555555",
                'account_number': "1123581321",
                'routing_number': "071101307",
            },
            "tos_accepted": True
        })

        serializer.is_valid()
        serializer.save(user=user)

    def handle(self, *args, **options):
        geolocator = Nominatim()

        User = get_user_model()  # noqa

        for place in options.get('places'):
            location = geolocator.geocode(place)

            if not location:
                continue

            print('Got a place in {}'.format(place))

            # create owner

            owner, created = User.objects.get_or_create(
                username='owner_{}'.format(slugify(place))
            )

            if created:
                print('Created owner {}'.format(owner.username))

                self.create_merchant(owner)

                print('Creating merchant')

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
