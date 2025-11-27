from rest_framework import routers
from .api_views import CalificacionViewSet, LogAuditoriaViewSet

router = routers.DefaultRouter()
router.register(r'calificaciones', CalificacionViewSet)
router.register(r'logs', LogAuditoriaViewSet)

urlpatterns = router.urls
