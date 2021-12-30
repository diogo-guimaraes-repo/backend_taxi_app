from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from backend_taxi_app.users.api.views import UserViewSet, ClientViewSet, CurrentUserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("clients", ClientViewSet)
router.register("me", CurrentUserViewSet)

app_name = "api"
urlpatterns = router.urls
