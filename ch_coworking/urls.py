from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from .views import ReservationViewSet, index, tables

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet, 'reservation')

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'tables', tables, name='tables'),
    url(r'api/', include(router.urls))
]
