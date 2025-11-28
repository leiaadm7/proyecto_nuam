from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Calificacion, LogAuditoria
from .forms import CalificacionForm, CargaMasivaForm
import csv
from io import TextIOWrapper

def home(request):
    return redirect('login')

@login_required
def dashboard(request):
    registros = Calificacion.objects.all().order_by('-fecha_registro')
    return render(request, 'calificaciones/dashboard.html', {'registros': registros})

@login_required
def historial(request):

    if not request.user.has_perm('calificaciones.view_logauditoria'):
        return redirect('dashboard')
        
    logs = LogAuditoria.objects.all().order_by('-fecha_hora')
    return render(request, 'calificaciones/historial.html', {'logs': logs})

@login_required
@permission_required('calificaciones.add_calificacion', raise_exception=True)
def crear_calificacion(request):
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.analista = request.user
            instancia.save()

            LogAuditoria.objects.create(
                usuario=request.user,
                accion="CREAR",
                detalle=f"Desde App Django: {instancia.pais} - {instancia.tipo}"
            )
            return redirect('dashboard')
    else:
        form = CalificacionForm()
    return render(request, 'calificaciones/formulario.html', {'form': form})

@login_required
@permission_required('calificaciones.change_calificacion', raise_exception=True)
def editar_calificacion(request, id):
    calificacion = get_object_or_404(Calificacion, id=id)
    if request.method == 'POST':
        form = CalificacionForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save()
            
            LogAuditoria.objects.create(
                usuario=request.user,
                accion="EDITAR",
                detalle=f"Desde App Django: Editó ID #{id}"
            )
            return redirect('dashboard')
    else:
        form = CalificacionForm(instance=calificacion)
    return render(request, 'calificaciones/formulario.html', {'form': form, 'titulo': 'Editar Calificación'})

@login_required
@permission_required('calificaciones.delete_calificacion', raise_exception=True)
def eliminar_calificacion(request, id):
    calificacion = get_object_or_404(Calificacion, id=id)
    
    LogAuditoria.objects.create(
        usuario=request.user,
        accion="ELIMINAR",
        detalle=f"Desde App Django: Borró ID #{id} ({calificacion.pais})"
    )
    
    calificacion.delete()
    return redirect('dashboard')

@login_required
@permission_required('calificaciones.add_calificacion', raise_exception=True)
def carga_masiva(request):
    if request.method == 'POST':
        form = CargaMasivaForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = TextIOWrapper(request.FILES['archivo_csv'].file, encoding='utf-8')
            csv_reader = csv.DictReader(archivo)
            for row in csv_reader:
                Calificacion.objects.create(
                    pais=row['pais'].strip().upper(),      
                    tipo=row['tipo'].strip().upper(),
                    monto_base=row['monto'],
                    factor=row['factor'],
                    analista=request.user
                )
            
            LogAuditoria.objects.create(
                usuario=request.user, 
                accion="CARGA MASIVA", 
                detalle="Procesó archivo CSV desde App Django"
            )
            return redirect('dashboard')
    else:
        form = CargaMasivaForm()
    
    return render(request, 'calificaciones/carga_masiva.html', {'form': form})