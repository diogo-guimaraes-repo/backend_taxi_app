from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TripsConfig(AppConfig):
    name = "backend_taxi_app.trips"
    verbose_name = _("Trips")

    def ready(self):
        try:
            import backend_taxi_app.trips.signals  # noqa F401
        except ImportError:
            pass
