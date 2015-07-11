from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import viewsets
from rest_framework.response import Response

from ch_coworking.models import Reservation

from .serializers import SingleReservationSerializer, ManyReservationsSerializer, AddReservationSerializer


class ReservationViewSet(viewsets.ViewSet):
    def list(self, request):
        reservations = Reservation.objects.filter(
            owner=self.request.user, date__gte=timezone.now().date())
        serializer = ManyReservationsSerializer(reservations, many=True)
        return Response(serializer.data)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        reservation = get_object_or_404(Reservation, pk=pk)
        serializer = SingleReservationSerializer(reservation)
        return Response(serializer.data)
