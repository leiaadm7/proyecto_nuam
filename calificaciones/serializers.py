from rest_framework import serializers
from .models import Calificacion, LogAuditoria

class CalificacionSerializer(serializers.ModelSerializer):
    analista_username = serializers.CharField(source="analista.username", read_only=True)
    pais_nombre = serializers.CharField(source='get_pais_display', read_only=True)
    tipo_nombre = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = Calificacion
        fields = [
            "id",
            "pais",
            "tipo",
            "monto_base",
            "factor",
            "fecha_registro",
            "analista",
            "analista_username",
        ]
        read_only_fields = ["analista", "fecha_registro"]


class LogAuditoriaSerializer(serializers.ModelSerializer):
    usuario_username = serializers.CharField(source="usuario.username", read_only=True)

    class Meta:
        model = LogAuditoria
        fields = [
            "id",
            "usuario",
            "usuario_username",
            "accion",
            "detalle",
            "fecha_hora",
        ]

