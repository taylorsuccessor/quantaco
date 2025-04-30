from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .ijson_views import ProcessLargeFileViewSet

router = DefaultRouter()
router.register(r"ijson", ProcessLargeFileViewSet, basename="ijson")

urlpatterns = [
    path("", include(router.urls)),
    path("", include("django_prometheus.urls")),
]
