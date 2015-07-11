import factory

from ch_users.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User
