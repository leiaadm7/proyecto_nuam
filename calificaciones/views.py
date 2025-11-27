from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Calificacion
from .forms import *
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
            return redirect('dashboard')
    else:
        form = CalificacionForm()
    return render(request, 'calificaciones/formulario.html', {'form': form})

def home(request):
    return redirect('login')

@login_required
def editar_calificacion(request, id):
    calificacion = get_object_or_404(Calificacion, id=id)
    if request.method == 'POST':
        form = CalificacionForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CalificacionForm(instance=calificacion)
    return render(request, 'calificaciones/formulario.html', {'form': form, 'titulo': 'Editar Calificación'})

@login_required
def eliminar_calificacion(request, id):
    calificacion = get_object_or_404(Calificacion, id=id)
    calificacion.delete()
    return redirect('dashboard')

@login_required
def carga_masiva(request):
    if request.method == 'POST':
        form = CargaMasivaForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = TextIOWrapper(request.FILES['archivo_csv'].file, encoding='utf-8')
            csv_reader = csv.DictReader(archivo)
            # 2. Recorrer cada fila del CSV
            contadores = 0
            for row in csv_reader:
                # 3. Guardar en la Base de Datos
                Calificacion.objects.create(
                    pais=row['pais'].strip().upper(),      
                    tipo=row['tipo'].strip().upper(),
                    monto_base=row['monto'],
                    factor=row['factor'],
                    analista=request.user # Guardamos quién hizo la carga (Auditoría)
                )
                contadores += 1
            return redirect('dashboard')
    else:
        form = CargaMasivaForm()
    
    return render(request, 'calificaciones/carga_masiva.html', {'form': form})