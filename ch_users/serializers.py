from __future__ import absolute_import
from __future__ import unicode_literals

from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        read_only_fields = ('email', 'date_joined', 'last_login')


class CreditCardSerializer(serializers.Serializer):
    last_4 = serializers.CharField(max_length=4)
    expiration_month = serializers.CharField(max_length=2)
    expiration_year = serializers.CharField(max_length=4)
    card_type = serializers.CharField(max_length=10)
    image_url = serializers.CharField(max_length=255)
    cardholder_name = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=255)
