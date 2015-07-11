from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException

from .models import Reservation, Table


class TimeOverlapException(APIException):
    status_code = status.HTTP_409_CONFLICT


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
