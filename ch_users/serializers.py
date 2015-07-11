import braintree

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException


class BraintreeAPIException(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = 'A braintree error occurred.'


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


class AddCreditCardSerializer(serializers.Serializer):
    nonce = serializers.CharField()

    def create(self, validated_data):
        user = validated_data['user']

        data = {
            'customer_id': user.get_braintree_customer_id(),
            'payment_method_nonce': validated_data['nonce'],
        }

        result = braintree.PaymentMethod.create(data)

        if not result.is_success:
            errors = [x.message for x in result.errors.deep_errors]

            raise BraintreeAPIException(errors)

        return result.payment_method
