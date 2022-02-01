from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from goticket.events.api.views import EventViewSet
from goticket.tickets.api.views import TicketCartViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("events", EventViewSet, basename="events")
router.register("tickets", TicketCartViewSet, basename="tickets")


app_name = "api"
urlpatterns = router.urls
