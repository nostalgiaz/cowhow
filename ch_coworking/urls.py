from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from .views import ReservationViewSet, CoworkingsViewSet, index, tables, table_activate, table_deactivate, table_price

from ch_users.views import MeView, TokenView, MeCreditCardsViewSet, MerchantViewSet

router = DefaultRouter()
router.register(r'coworkings', CoworkingsViewSet, 'coworking')
router.register(r'reservations', ReservationViewSet, 'reservation')
router.register(r'me/credit-cards', MeCreditCardsViewSet, 'credit-cards')
router.register(r'me/merchant', MerchantViewSet, 'merchant')

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'tables$', tables, name='tables'),
    url(r'tables/(?P<table_id>[0-9]+)/activate$', table_activate, name='table_activate'),
    url(r'tables/(?P<table_id>[0-9]+)/deactivate$', table_deactivate, name='table_deactivate'),
    url(r'tables/(?P<table_id>[0-9]+)/price$', table_price, name='table_price'),
    url(r'api/me/token/$', TokenView.as_view()),
    url(r'api/me/$', MeView.as_view()),
    url(r'api/', include(router.urls)),
]
