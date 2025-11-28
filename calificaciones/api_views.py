from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models 
from .models import Calificacion, LogAuditoria
from .serializers import CalificacionSerializer, LogAuditoriaSerializer

class EsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="ADMIN").exists()

class EsInterno(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="INTERNO").exists()

class EsAuditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="AUDITOR").exists()

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all().order_by("-fecha_registro")
    serializer_class = CalificacionSerializer
    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [EsAdmin]
        elif self.action in ['create', 'update', 'partial_update']:
            permission_classes = [EsAdmin | EsInterno]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


    def perform_create(self, serializer):
        instancia = serializer.save(analista=self.request.user)
        
        detalle = (
            f"NUEVO #{instancia.id} | "
            f"País: {instancia.get_pais_display()} | "
            f"Tipo: {instancia.get_tipo_display()} | "
            f"Monto: ${instancia.monto_base} | "
            f"Factor: {instancia.factor}"
        )
        self.registrar_log("CREAR", detalle)

    def perform_update(self, serializer):
        instancia = serializer.save()
        
        detalle = (
            f"EDITADO #{instancia.id} | "
            f"País: {instancia.get_pais_display()} | "
            f"Tipo: {instancia.get_tipo_display()} | "
            f"Nuevo Monto: ${instancia.monto_base} | "
            f"Nuevo Factor: {instancia.factor}"
        )
        self.registrar_log("EDITAR", detalle)

    def perform_destroy(self, instance):
        detalle = (
            f"ELIMINADO #{instance.id} | "
            f"País: {instance.get_pais_display()} | "
            f"Monto Perdido: ${instance.monto_base}"
        )
        self.registrar_log("ELIMINAR", detalle)
        instance.delete()

    def registrar_log(self, accion, detalle):
        LogAuditoria.objects.create(
            usuario=self.request.user, 
            accion=accion, 
            detalle=detalle
        )

    @action(detail=False, methods=["get"])
    def resumen_por_pais(self, request):
        data = Calificacion.objects.values("pais").annotate(total=models.Count("id"))
        return Response(list(data))

class LogAuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogAuditoria.objects.all().order_by("-fecha_hora")
    serializer_class = LogAuditoriaSerializer
    permission_classes = [EsAdmin | EsAuditor]

class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        grupo = "NINGUNO"
        if request.user.groups.filter(name='ADMIN').exists():
            grupo = "ADMIN"
        elif request.user.groups.filter(name='INTERNO').exists():
            grupo = "INTERNO"
        elif request.user.groups.filter(name='AUDITOR').exists():
            grupo = "AUDITOR"
        
        return Response({"username": request.user.username, "grupo": grupo})