import braintree

from datetime import datetime, date
from decimal import Decimal

from rest_framework import serializers, pagination

from .models import Reservation, Table
from .paginators import ESPaginator

from core.utils import TimeOverlapException, BraintreeAPIException


class SingleReservationSerializer(serializers.ModelSerializer):
    lng = serializers.FloatField(source='table.coworking.lng')
    lat = serializers.FloatField(source='table.coworking.lat')

    class Meta:
        model = Reservation
        fields = ['pk', 'date', 'from_hour', 'to_hour', 'lat', 'lng']


class ManyReservationsSerializer(SingleReservationSerializer):
    pass


class AddReservationSerializer(serializers.Serializer):
    table = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all())
    from_hour = serializers.TimeField()
    to_hour = serializers.TimeField()
    date = serializers.DateField()
    payment_token = serializers.CharField()

    def validate(self, data):
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

        from_time = datetime.combine(date.today(), validated_data['from_hour'])
        to_time = datetime.combine(date.today(), validated_data['to_hour'])

        hours = (to_time - from_time).seconds / 3600

        amount = table.price * Decimal(hours)

        result = braintree.Transaction.sale({
            'amount': amount,
            'payment_method_token': validated_data.pop('payment_token'),
            'options': {
                'submit_for_settlement': True
            }
        })

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


class ESCoworkingSerializer(serializers.Serializer):
    location = ESLocationField()
    name = serializers.ReadOnlyField()


class PagedCoworkingSerializer(pagination.PageNumberPagination):
    def __init__(self, result, request, n):
        paginator = ESPaginator(result, n)

        self.request = request
        self.page = paginator.page(request.GET.get('page', 1))
