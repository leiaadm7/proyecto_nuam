from .models import LogAuditoria
import json

def registrar_log(usuario, accion, detalle_dict):
    LogAuditoria.objects.create(
        usuario=usuario,
        accion=accion,
        detalle=json.dumps(detalle_dict, indent=2)
    )