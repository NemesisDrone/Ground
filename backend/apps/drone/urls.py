from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"api/drone/images", views.DroneImagesViewSet, basename="drone_images")
router.register(r"api/drone/settings/models", views.DroneSettingsModelViewSet, basename="drone_settings_models")

urlpatterns = [
    path("api/drone/settings/", views.get_drone_settings),
    path("api/drone/settings/select-model/", views.update_selected_drone_settings_model),
]

urlpatterns += router.urls