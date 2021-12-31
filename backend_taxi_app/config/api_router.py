from django.conf import settings
from rest_framework import routers
from backend_taxi_app.users.api.views import UserViewSet, ClientViewSet, CurrentUserViewSet


class CustomRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'patch': 'partial_update',
            },
            name='{basename}',
            detail=False,
            initkwargs={'suffix': ''}
        ),
    ]


if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

me_router = CustomRouter()

router.register("users", UserViewSet)
router.register("clients", ClientViewSet)
me_router.register("me", CurrentUserViewSet)


app_name = "api"
urlpatterns = router.urls + me_router.urls
