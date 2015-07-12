from django.core.urlresolvers import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from . import factories


class TestApiReservationWorkflow(APITestCase):
    def test_flow(self):
        user = factories.UserFactory()
        owner = factories.UserFactory()
        table = factories.TableFactory(coworking__owner=owner)

        self.client.force_authenticate(user=owner)

        data = {
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
        }

        url = reverse('merchant-list')

        self.client.post(url, data, format='json')

        self.client.force_authenticate(user=user)

        url = reverse('credit-cards-list')
        response = self.client.post(url, {
            'nonce': 'fake-valid-nonce'
        }, format='json')

        token = response.data['token']

        url = reverse('reservation-list')
        response = self.client.post(url, {
            'table': table.pk,
            'date': timezone.now().date(),
            'from_hour': '13:00',
            'to_hour': '15:00',
            'payment_token': token,
        }, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_flow_nonce(self):
        user = factories.UserFactory()
        owner = factories.UserFactory()
        table = factories.TableFactory(coworking__owner=owner)

        self.client.force_authenticate(user=owner)

        data = {
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
        }

        url = reverse('merchant-list')

        self.client.post(url, data, format='json')

        self.client.force_authenticate(user=user)

        url = reverse('reservation-list')
        response = self.client.post(url, {
            'table': table.pk,
            'date': timezone.now().date(),
            'from_hour': '13:00',
            'to_hour': '15:00',
            'payment_nonce': 'fake-valid-nonce'
        }, format='json')

        assert response.status_code == status.HTTP_201_CREATED
