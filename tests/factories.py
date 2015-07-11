import random
from datetime import time

import factory
import factory.fuzzy

from django.utils import timezone

from ch_coworking.models import Coworking, Table, Reservation
from ch_users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: "user_%d" % n)

    class Meta:
        model = User


class CoworkingFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    lat = factory.fuzzy.FuzzyDecimal(-90, 90)
    lng = factory.fuzzy.FuzzyDecimal(-180, 180)

    opening = factory.LazyAttribute(lambda obj: time(random.randint(6, 10), 0))
    closing = factory.LazyAttribute(lambda obj: time(random.randint(18, 22), 0))

    class Meta:
        model = Coworking


class TableFactory(factory.django.DjangoModelFactory):
    price = factory.fuzzy.FuzzyDecimal(30, 90)
    coworking = factory.SubFactory(CoworkingFactory)

    class Meta:
        model = Table


class ReservationFactory(factory.django.DjangoModelFactory):
    table = factory.SubFactory(TableFactory)
    owner = factory.SubFactory(UserFactory)
    from_hour = factory.LazyAttribute(lambda obj: time(random.randint(6, 10), 0))
    to_hour = factory.LazyAttribute(lambda obj: time(random.randint(18, 22), 0))

    date = factory.LazyAttribute(lambda obj: timezone.now().date())

    class Meta:
        model = Reservation
