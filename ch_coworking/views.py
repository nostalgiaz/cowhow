from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from elasticsearch_dsl import Search

from ch_coworking.models import Reservation

from .helpers import ChHelpers
from .serializers import (
    SingleReservationSerializer, ManyReservationsSerializer, AddReservationSerializer,
    PagedCoworkingSerializer, ESCoworkingSerializer
)


class CoworkingsViewSet(viewsets.ViewSet):
    def list(self, request):
        client = ChHelpers.get_es()

        s = Search(
            using=client,
            index=settings.ELASTICSEARCH['index'],
            doc_type=settings.ELASTICSEARCH['doc_type']
        )

        amenities = request.GET.getlist('amenities')

        if len(amenities) > 0:
            s = s.filter('terms', amenities=amenities)

        top_left = request.GET.get('top_left', False)
        bottom_right = request.GET.get('bottom_right', False)

        if top_left and bottom_right:
            a, b = top_left.split(',')
            c, d = bottom_right.split(',')

            s = s.filter('geo_bounding_box', location={
                'top_left': {
                    'lat': a,
                    'lon': b
                },
                'bottom_right': {
                    'lat': c,
                    'lon': d
                }
            })

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
