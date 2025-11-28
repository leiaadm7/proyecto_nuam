from django.urls import path, include
from rest_framework import routers
from .api_views import CalificacionViewSet, LogAuditoriaViewSet

router = routers.DefaultRouter()
router.register(r'calificaciones', CalificacionViewSet)
router.register(r'historial', LogAuditoriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]