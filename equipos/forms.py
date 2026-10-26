from django import forms
from .models import Equipo, Jugador, Pais


class FormsEquipo(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre', 'imagen', 'pais', 'ciudad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pais': forms.Select(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FormsJugador(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = ['nombre', 'imagen', 'pais_nacimiento', 'posicion', 'activo', 'descripcion', 'equipo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pais_nacimiento': forms.Select(attrs={'class': 'form-control'}),
            'posicion': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'equipo': forms.Select(attrs={'class': 'form-control'}),
        }


class FormsPais(forms.ModelForm):
    class Meta:
        model = Pais
        fields = ['nombre', 'imagen', 'continente']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'continente': forms.TextInput(attrs={'class': 'form-control'}),
        }