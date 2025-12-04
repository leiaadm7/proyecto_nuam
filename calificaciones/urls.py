from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views
from . import views
from . import api_views 

router = routers.DefaultRouter()
router.register(r'calificaciones', api_views.CalificacionViewSet)
router.register(r'historial', api_views.LogAuditoriaViewSet)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='calificaciones/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('nuevo/', views.crear_calificacion, name='nuevo'),
    path('editar/<int:id>/', views.editar_calificacion, name='editar'),
    path('eliminar/<int:id>/', views.eliminar_calificacion, name='eliminar'),
    path('carga-masiva/', views.carga_masiva, name='carga_masiva'),
    path('historial-web/', views.historial, name='historial_web'), 
]