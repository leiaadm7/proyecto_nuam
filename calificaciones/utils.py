from .models import LogAuditoria
import json
from django.contrib.auth.models import Group

def registrar_log(usuario, accion, detalle_dict):
    LogAuditoria.objects.create(
        usuario=usuario,
        accion=accion,
        detalle=json.dumps(detalle_dict, indent=2)
    )

def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

