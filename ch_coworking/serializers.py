import braintree

from datetime import datetime, date
from decimal import Decimal

from rest_framework import serializers, pagination
from rest_framework.exceptions import ValidationError

from .models import Reservation, Table, Coworking
from .paginators import ESPaginator

from core.utils import TimeOverlapException, BraintreeAPIException


class SingleReservationSerializer(serializers.ModelSerializer):
    lng = serializers.FloatField(source='table.coworking.lng')
    lat = serializers.FloatField(source='table.coworking.lat')
    host_name = serializers.CharField(source='table.coworking.name')

    class Meta:
        model = Reservation
        fields = [
            'pk', 'date', 'from_hour', 'to_hour', 'lat', 'lng', 'host_name',
        ]


class ManyReservationsSerializer(SingleReservationSerializer):
    pass


class CoworkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coworking


class AddReservationSerializer(serializers.Serializer):
    table = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all())
    from_hour = serializers.TimeField()
    to_hour = serializers.TimeField()
    date = serializers.DateField()
    payment_token = serializers.CharField(required=False)
    payment_nonce = serializers.CharField(required=False)

    def validate(self, data):
        if not data.get('payment_nonce', False) and not data.get('payment_token', False):
            raise ValidationError('You must provide at least a token or a nonce')

        a = data['from_hour']
        b = data['to_hour']

        date = data['date']
        table = data['table']

        # http://stackoverflow.com/questions/325933/determine-whether-two-date-ranges-overlap
        # (EndB >= StartA)  and  (StartB <= EndA)

        q = Reservation.objects.filter(
            table=table,
            date=date,
            from_hour__lte=a,
            to_hour__gte=b,
        )

        if q.count() > 0:
            raise TimeOverlapException('Time overlaps!')

        return data

    def create(self, validated_data):
        table = validated_data['table']

        assert table.coworking.owner.braintree_merchant_id

        from_time = datetime.combine(date.today(), validated_data['from_hour'])
        to_time = datetime.combine(date.today(), validated_data['to_hour'])

        hours = (to_time - from_time).seconds / 3600

        amount = table.price * Decimal(hours)

        data = {
            'amount': amount,
            'merchant_account_id': table.coworking.owner.braintree_merchant_id,
            'service_fee_amount': '0.1',
            'options': {
                'submit_for_settlement': True
            }
        }

        if validated_data.get('payment_token', ''):
            data['payment_method_token'] = validated_data.pop('payment_token')
        else:
            data['payment_method_nonce'] = validated_data.pop('payment_nonce')

        result = braintree.Transaction.sale(data)

        if not result.is_success:
            errors = [x.message for x in result.errors.deep_errors]

            raise BraintreeAPIException(errors)

        validated_data['transaction_id'] = result.transaction.id

        return Reservation.objects.create(**validated_data)


class ESLocationField(serializers.ReadOnlyField):
    def to_representation(self, obj):
        return {
            'latitude': obj['lat'],
            'longitude': obj['lon'],
        }


class ESPhotosField(serializers.ReadOnlyField):
    def to_representation(self, obj):
        return list(obj)


class ESAmenitiesField(serializers.ReadOnlyField):
    def to_representation(self, obj):
        return list(obj)


class ESTablesField(serializers.ReadOnlyField):
    def to_representation(self, obj):
        return [{
            'price': o.price,
            'name': o.name,
            'pk': o.pk
        } for o in obj]


class ESCoworkingSerializer(serializers.Serializer):
    location = ESLocationField()
    name = serializers.ReadOnlyField()
    amenities = ESAmenitiesField()
    photos = ESPhotosField()
    tables = ESTablesField()
    id = serializers.ReadOnlyField(source='meta.id')


class PagedCoworkingSerializer(pagination.PageNumberPagination):
    def __init__(self, result, request, n):
        paginator = ESPaginator(result, n)

        self.request = request
        self.page = paginator.page(request.GET.get('page', 1))
