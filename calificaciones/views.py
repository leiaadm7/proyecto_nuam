from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Calificacion, LogAuditoria
from .forms import *
from .utils import registrar_log
import csv
from io import TextIOWrapper


@login_required
def dashboard(request):
    registros = Calificacion.objects.all().order_by('-fecha_registro')
    return render(request, 'calificaciones/dashboard.html', {'registros': registros})


@login_required
def crear_calificacion(request):
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.analista = request.user
            obj.save()

            # AUDITORÍA
            registrar_log(
                usuario=request.user,
                accion="CREAR",
                detalle_dict={
                    "pais": obj.pais,
                    "tipo": obj.tipo,
                    "monto_base": str(obj.monto_base),
                    "factor": str(obj.factor)
                }
            )

            return redirect('dashboard')
    else:
        form = CalificacionForm()

    return render(request, 'calificaciones/formulario.html', {'form': form})


def home(request):
    return redirect('login')


@login_required
def editar_calificacion(request, id):
    calificacion = get_object_or_404(Calificacion, id=id)
    datos_antes = {
        "pais": calificacion.pais,
        "tipo": calificacion.tipo,
        "monto_base": str(calificacion.monto_base),
        "factor": str(calificacion.factor),
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
                        "monto_base": str(nuevo_obj.monto_base),
                        "factor": str(nuevo_obj.factor)
                    }
                }
            )

            return redirect('dashboard')

    else:
        form = CalificacionForm(instance=calificacion)

    return render(
        request,
        'calificaciones/formulario.html',
        {'form': form, 'titulo': 'Editar Calificación'}
    )


@login_required
def eliminar_calificacion(request, id):
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
    return redirect('dashboard')


@login_required
def carga_masiva(request):
    if request.method == 'POST':
        form = CargaMasivaForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = TextIOWrapper(request.FILES['archivo_csv'].file, encoding='utf-8')
            csv_reader = csv.DictReader(archivo)

            contador = 0
            for row in csv_reader:
                Calificacion.objects.create(
                    pais=row['pais'].strip().upper(),
                    tipo=row['tipo'].strip().upper(),
                    monto_base=row['monto'],
                    factor=row['factor'],
                    analista=request.user
                )
                contador += 1
            registrar_log(
                usuario=request.user,
                accion="CARGA MASIVA",
                detalle_dict={
                    "total_registros": contador
                }
            )

            return redirect('dashboard')
    else:
        form = CargaMasivaForm()

    return render(request, 'calificaciones/carga_masiva.html', {'form': form})


@login_required
def historial(request):
    logs = LogAuditoria.objects.all().order_by('-fecha_hora')
    return render(request, 'calificaciones/historial.html', {'logs': logs})
