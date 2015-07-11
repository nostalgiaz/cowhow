from rest_framework import serializers

from .models import Reservation, Table


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
