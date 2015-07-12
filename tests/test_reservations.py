from datetime import time

from django.core.urlresolvers import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

import mock

from . import factories


class TestApiReservationCreation(APITestCase):
    def test_fails_if_not_logged(self):
        url = reverse('reservation-list')
        response = self.client.post(url, {}, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_fails_if_table_is_not_available(self):
        user = factories.UserFactory()
        table = factories.TableFactory()

        factories.ReservationFactory(
            table=table,
            date=timezone.now().date(),
            from_hour=time(10, 00),
            to_hour=time(20, 00),
        )

        self.client.force_authenticate(user=user)

        url = reverse('reservation-list')
        response = self.client.post(url, {
            'table': table.pk,
            'date': timezone.now().date(),
            'from_hour': '10:00',
            'to_hour': '15:00',
            'payment_token': 'fake-valid-token'
        }, format='json')

        assert response.status_code == status.HTTP_409_CONFLICT

    @mock.patch('braintree.Transaction.sale')
    def test_fails_does_not_fail_on_same_day(self, m):
        user = factories.UserFactory()
        owner = factories.UserFactory(braintree_merchant_id='fake_id')
        table = factories.TableFactory(coworking__owner=owner)

        factories.ReservationFactory(
            table=table,
            date=timezone.now().date(),
            from_hour=time(10, 00),
            to_hour=time(12, 00),
        )

        m.return_value.is_success = True
        m.return_value.transaction.id = '123'

        self.client.force_authenticate(user=user)

        url = reverse('reservation-list')
        response = self.client.post(url, {
            'table': table.pk,
            'date': timezone.now().date(),
            'from_hour': '13:00',
            'to_hour': '15:00',
            'payment_token': 'fake-valid-token',
        }, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    @mock.patch('braintree.Transaction.sale')
    def test_add(self, m):
        user = factories.UserFactory()
        owner = factories.UserFactory(braintree_merchant_id='fake_id')
        table = factories.TableFactory(coworking__owner=owner)

        m.return_value.is_success = True
        m.return_value.transaction.id = '123'

        self.client.force_authenticate(user=user)

        url = reverse('reservation-list')
        response = self.client.post(url, {
            'table': table.pk,
            'date': timezone.now().date(),
            'from_hour': '10:00',
            'to_hour': '15:00',
            'payment_token': 'fake-valid-token',
        }, format='json')

        assert response.status_code == status.HTTP_201_CREATED
