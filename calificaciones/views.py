from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Calificacion, LogAuditoria
from .forms import *
from .utils import registrar_log
import csv
from io import TextIOWrapper

def home(request):
    """
    Entra a / y redirige al login.
    """
    return redirect('login')

@login_required
def dashboard(request):
    """
    Vista principal con la tabla de calificaciones.
    """
    registros = Calificacion.objects.all().order_by('-fecha_registro')
    return render(request, 'calificaciones/dashboard.html', {'registros': registros})


@login_required
def crear_calificacion(request):
    """
    Crear una nueva calificación desde el formulario HTML.
    """
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.analista = request.user
            obj.save()

            # Auditoría
            registrar_log(
                usuario=request.user,
                accion="CREAR",
                detalle_dict={
                    "pais": obj.pais,
                    "tipo": obj.tipo,
                    "monto_base": float(obj.monto_base),
                    "factor": float(obj.factor)
                }
            )

            messages.success(request, "Calificación creada correctamente.")
            return redirect('dashboard')
    else:
        form = CalificacionForm()

    return render(request, 'calificaciones/formulario.html', {'form': form})


@login_required
def editar_calificacion(request, id):
    """
    Editar cualquier calificación existente.
    """
    calificacion = get_object_or_404(Calificacion, id=id)

    datos_antes = {
        "pais": calificacion.pais,
        "tipo": calificacion.tipo,
        "monto_base": float(calificacion.monto_base),
        "factor": float(calificacion.factor),
    }

    if request.method == 'POST':
        form = CalificacionForm(request.POST, instance=calificacion)
        if form.is_valid():
            nuevo_obj = form.save()

            registrar_log(
                usuario=request.user,
                accion="EDITAR",
                detalle_dict={
                    "antes": datos_antes,
                    "despues": {
                        "pais": nuevo_obj.pais,
                        "tipo": nuevo_obj.tipo,
                        "monto_base": float(nuevo_obj.monto_base),
                        "factor": float(nuevo_obj.factor)
                    }
                }
            )

            messages.success(request, "Calificación actualizada correctamente.")
            return redirect('dashboard')

    else:
        form = CalificacionForm(instance=calificacion)

    return render(request, 'calificaciones/formulario.html', {
        'form': form,
        'titulo': 'Editar Calificación'
    })


@login_required
def eliminar_calificacion(request, id):
    """
    Eliminar una calificación.
    """
    calificacion = get_object_or_404(Calificacion, id=id)

    registrar_log(
        usuario=request.user,
        accion="ELIMINAR",
        detalle_dict={
            "id": calificacion.id,
            "pais": calificacion.pais,
            "tipo": calificacion.tipo
        }
    )

    calificacion.delete()
    messages.success(request, "Calificación eliminada correctamente.")
    return redirect('dashboard')


@login_required
def carga_masiva(request):
    """
    Subida masiva mediante CSV.
    Campos esperados:
    pais,tipo,monto,factor
    """
    if request.method == 'POST':
        form = CargaMasivaForm(request.POST, request.FILES)

        if form.is_valid():

            archivo = TextIOWrapper(
                request.FILES['archivo_csv'].file,
                encoding='utf-8'
            )

            csv_reader = csv.DictReader(archivo)

            contador = 0
            for row in csv_reader:
                Calificacion.objects.create(
                    pais=row['pais'].strip().upper(),
                    tipo=row['tipo'].strip().upper(),
                    monto_base=float(row['monto']),
                    factor=float(row['factor']),
                    analista=request.user
                )
                contador += 1

            registrar_log(
                usuario=request.user,
                accion="CARGA MASIVA",
                detalle_dict={"total_registros": contador}
            )

            messages.success(request, f"Carga masiva exitosa: {contador} registros.")
            return redirect('dashboard')

    else:
        form = CargaMasivaForm()

    return render(request, 'calificaciones/carga_masiva.html', {'form': form})


@login_required
def historial(request):
    """
    Muestra el historial completo de acciones registradas.
    """
    logs = LogAuditoria.objects.all().order_by('-fecha_hora')
    return render(request, 'calificaciones/historial.html', {'logs': logs})
