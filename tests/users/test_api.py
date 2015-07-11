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
