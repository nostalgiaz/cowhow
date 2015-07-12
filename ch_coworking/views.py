from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from elasticsearch_dsl import Search

from ch_coworking.models import Reservation, Table, Coworking

from . import utils
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

        amenities = request.GET.getlist('amenities[]')

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

        obj = serializer.save(owner=request.user)

        serializer = SingleReservationSerializer(obj)

        utils.turn_lights_on()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        reservation = get_object_or_404(Reservation, pk=pk)
        serializer = SingleReservationSerializer(reservation)
        return Response(serializer.data)


class CowhowIndexView(TemplateView):
    template_name = "ch_coworking/index.html"

index = login_required(CowhowIndexView.as_view())


class CowhowTablesView(ListView):
  template_name = "admin/tables.html"

  def get_queryset(self):
      return Table.objects.filter(coworking__owner=self.request.user)

  def get_context_data(self, **kwargs):
      context = super(CowhowTablesView, self).get_context_data(**kwargs)
      context['coworking'] = Coworking.objects.filter(owner=self.request.user)[0]
      context['tables_active'] = context['coworking'].tables.filter(active=True).count()
      return context

tables = login_required(CowhowTablesView.as_view())

def table_activate(request, table_id):
  table = get_object_or_404(Table,pk=table_id)
  table.active=True
  table.save()
  return HttpResponse(str(table.active).lower())

def table_deactivate(request, table_id):
  table = get_object_or_404(Table,pk=table_id)
  table.active=False
  table.save()
  return HttpResponse(str(table.active).lower())

def table_price(request, table_id):
  table = get_object_or_404(Table,pk=table_id)
  if 'val' in request.GET:
    table.price=request.GET['val']
    table.save()
  return HttpResponse(table.price)
