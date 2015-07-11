from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from . import factories


class TestApiReservationCreation(APITestCase):
    def test_fails_if_not_logged(self):
        url = reverse('reservations-list')
        response = self.client.post(url, {}, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add(self):
        user = factories.UserFactory()

        self.client.force_authenticate(user=user)

        url = reverse('reservations-list')
        response = self.client.post(url, {}, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN
