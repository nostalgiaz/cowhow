from __future__ import absolute_import
from __future__ import unicode_literals

from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        read_only_fields = ('email', 'date_joined', 'last_login')
