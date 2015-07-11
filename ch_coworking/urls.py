from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from .views import ReservationViewSet, index, tables, table_activate, table_deactivate

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet, 'reservation')

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'tables$', tables, name='tables'),
    url(r'tables/(?P<table_id>[0-9]+)/activate$', table_activate, name='table_activate'),
    url(r'tables/(?P<table_id>[0-9]+)/deactivate$', table_deactivate, name='table_deactivate'),
    url(r'api/', include(router.urls))
]
