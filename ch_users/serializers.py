import braintree

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import serializers

from core.utils import BraintreeAPIException


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


class AddressSerializer(serializers.Serializer):
    street_address = serializers.CharField()
    locality = serializers.CharField()
    region = serializers.CharField()
    postal_code = serializers.CharField()


class IndividualSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    date_of_birth = serializers.DateField()
    address = AddressSerializer()


class FundingSerializer(serializers.Serializer):
    descriptor = serializers.CharField()
    email = serializers.EmailField()
    account_number = serializers.CharField()
    routing_number = serializers.CharField()


class MerchantAccountSerializer(serializers.Serializer):
    individual = IndividualSerializer()
    funding = FundingSerializer()
    tos_accepted = serializers.BooleanField()

    def create(self, validated_data):
        user = validated_data.pop('user')

        validated_data['master_merchant_account_id'] = settings.BRAINTREE_MERCHANT_FRIENDLY_ID
        validated_data['funding']['destination'] = braintree.MerchantAccount.FundingDestination.Email

        result = braintree.MerchantAccount.create(validated_data)

        if not result.is_success:
            errors = [x.message for x in result.errors.deep_errors]

            raise BraintreeAPIException(errors)

        user.braintree_merchant_id = result.merchant_account.id
        user.save()

        return result.merchant_account
