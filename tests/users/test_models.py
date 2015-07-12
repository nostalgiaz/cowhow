from django.test import TestCase

import mock

from .. import factories


class TestUserModel(TestCase):
    @mock.patch('braintree.Customer.create')
    def test_creates_customer_if_no_id(self, m):
        user = factories.UserFactory()

        assert not user.braintree_customer_id

        m.return_value.is_success = True
        m.return_value.customer.id = '123'

        customer_id = user.get_braintree_customer_id()

        assert m.called
        assert customer_id == '123'
