from django.contrib import admin
from .models import Calificacion, LogAuditoria

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'pais', 'tipo', 'monto_base', 'analista', 'fecha_registro')
    list_filter = ('pais', 'tipo')
    search_fields = ('pais', 'analista__username')

@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('fecha_hora', 'usuario', 'accion', 'detalle')
    list_filter = ('accion', 'usuario')
    search_fields = ('detalle', 'usuario__username')
    readonly_fields = ('fecha_hora', 'usuario', 'accion', 'detalle') 