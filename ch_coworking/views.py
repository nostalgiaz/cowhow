from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from elasticsearch_dsl import Search, Q

from ch_coworking.models import Reservation

from .helpers import ChHelpers
from .serializers import (
    SingleReservationSerializer, ManyReservationsSerializer, AddReservationSerializer,
    PagedCoworkingSerializer, ESCoworkingSerializer
)


class CoworkingsViewSet(viewsets.ViewSet):
    def list(self, request):
        client = ChHelpers.get_es()

        s = Search(using=client, index=settings.ELASTICSEARCH['index'])

        serializer = PagedCoworkingSerializer(s, request, 100)
        data = ESCoworkingSerializer(data=serializer.page, many=True)

        data.is_valid()

        return serializer.get_paginated_response(data.data)


class ReservationViewSet(viewsets.ViewSet):
    def list(self, request):
        reservations = Reservation.objects.filter(
            owner=self.request.user, date__gte=timezone.now().date())
        serializer = ManyReservationsSerializer(reservations, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = AddReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(owner=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        reservation = get_object_or_404(Reservation, pk=pk)
        serializer = SingleReservationSerializer(reservation)
        return Response(serializer.data)


class CowhowIndexView(TemplateView):
    template_name = "ch_coworking/index.html"

index = login_required(CowhowIndexView.as_view())
