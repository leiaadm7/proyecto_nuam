from django import forms
from .models import Calificacion

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['pais', 'tipo', 'monto_base', 'factor']
        widgets = {
            'pais': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'monto_base': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'factor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.19'}),
        }

class CargaMasivaForm(forms.Form):
    archivo_csv = forms.FileField(
        label="Selecciona archivo CSV",
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text="El archivo debe tener las columnas: pais, tipo, monto, factor"
    )