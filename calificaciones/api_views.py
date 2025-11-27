from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models 
from .models import Calificacion, LogAuditoria
from .serializers import CalificacionSerializer, LogAuditoriaSerializer

class EsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="ADMIN").exists()


class EsInterno(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="INTERNO").exists()


class EsAuditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="AUDITOR").exists()

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all().order_by("-fecha_registro")
    serializer_class = CalificacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(analista=self.request.user)

    @action(detail=False, methods=["get"])
    def resumen_por_pais(self, request):
        data = (
            Calificacion.objects
            .values("pais")
            .order_by("pais")
            .annotate(total=models.Count("id"))
        )
        return Response(list(data))


class LogAuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogAuditoria.objects.all().order_by("-fecha_hora")
    serializer_class = LogAuditoriaSerializer
    permission_classes = [permissions.IsAuthenticated]
