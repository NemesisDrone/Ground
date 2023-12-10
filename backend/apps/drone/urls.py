from django.urls import path
from rest_framework import routers

from . import views

urlpatterns = [
    path("api/drone/settings/", views.get_drone_settings),
    path("api/drone/settings/update/", views.update_drone_settings),
]
