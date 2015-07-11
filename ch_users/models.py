import braintree

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    braintree_customer_id = models.CharField(max_length=255, blank=True)

    def get_braintree_customer_id(self):
        """
        Returns user's braintree customer if any. If not id is
        found we will create a new braintree customer
        """

        if self.braintree_customer_id:
            return self.braintree_customer_id

        result = braintree.Customer.create({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        })

        if result.is_success:
            self.braintree_customer_id = result.customer.id
            self.save()

            return self.braintree_customer_id
        else:
            raise ValueError
