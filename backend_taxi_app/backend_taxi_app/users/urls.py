from django.urls import path

from backend_taxi_app.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    client_signup_view,
    driver_signup_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:email>/", view=user_detail_view, name="detail"),
    path("client/signup/", view=client_signup_view, name="client-signup"),
    path("driver/signup/", view=driver_signup_view, name="driver-signup"),
]
