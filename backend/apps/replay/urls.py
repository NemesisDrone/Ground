from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"api/replay/sessions", views.ReplaySessionViewset, basename="replay_sessions")

urlpatterns = [
]
urlpatterns += router.urls