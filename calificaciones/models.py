from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Calificacion(models.Model):
    PAISES = [
        ('CHILE', 'Chile'),
        ('PERU', 'Perú'),
        ('COLOMBIA', 'Colombia'),
    ]
    
    TIPO_IMPUESTO = [
        ('IVA', 'IVA / IGV'),
        ('RENTA', 'Impuesto a la Renta'),
        ('ADUANA', 'Impuesto Aduanero'),
    ]

    pais = models.CharField(max_length=20, choices=PAISES, verbose_name="País")
    tipo = models.CharField(max_length=20, choices=TIPO_IMPUESTO, verbose_name="Tipo de Impuesto")
    monto_base = models.DecimalField(max_digits=12, decimal_places=2)
    factor = models.DecimalField(max_digits=5, decimal_places=4, help_text="Ej: 0.19 para 19%")
    fecha_registro = models.DateTimeField(default=timezone.now)
    analista = models.ForeignKey(User, on_delete=models.CASCADE) # Auditoría: quién lo hizo

    def __str__(self):
        return f"{self.pais} - {self.tipo}"

class LogAuditoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=50) 
    fecha_hora = models.DateTimeField(auto_now_add=True)
    detalle = models.TextField() 

    def __str__(self):
        return f"{self.usuario} - {self.accion} - {self.fecha_hora}"
