from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .. import factories


class TestCreditCardApi(APITestCase):
    def test_add_fails_with_fake_nonce(self):
        user = factories.UserFactory()

        self.client.force_authenticate(user=user)

        url = reverse('credit-cards-list')
        response = self.client.post(url, {
            'nonce': 'asd'
        }, format='json')

        assert response.status_code == status.HTTP_502_BAD_GATEWAY

    def test_add_works(self):
        user = factories.UserFactory()

        self.client.force_authenticate(user=user)

        url = reverse('credit-cards-list')
        response = self.client.post(url, {
            'nonce': 'fake-valid-nonce'
        }, format='json')

        assert response.status_code == status.HTTP_201_CREATED


class TestMerchantApi(APITestCase):
    def test_adding_info(self):
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

        user = factories.UserFactory()

        self.client.force_authenticate(user=user)

        url = reverse('merchant-list')

        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
