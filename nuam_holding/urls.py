from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from calificaciones import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='calificaciones/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('nuevo/', views.crear_calificacion, name='nuevo'),
    path('editar/<int:id>/', views.editar_calificacion, name='editar'),
    path('eliminar/<int:id>/', views.eliminar_calificacion, name='eliminar'),
    path('carga-masiva/', views.carga_masiva, name='carga_masiva'),
    path('historial/', views.historial, name='historial'),

]