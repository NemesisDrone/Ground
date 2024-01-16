from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# router.register(r"api/drone/images", views.DroneImagesViewSet, basename="drone_images")

urlpatterns = [
    # path("api/drone/settings/", views.get_drone_settings),
]

urlpatterns += router.urls