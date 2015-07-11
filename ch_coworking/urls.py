from .views import ReservationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet, 'reservation')
urlpatterns = router.urls