import unicodedata
from django import forms
from .models import Equipo, Jugador, Pais

def normalizar_texto(texto):
    if not texto:
        return ""
    descompuesto = unicodedata.normalize('NFKD', str(texto))
    sin_acentos = ''.join(c for c in descompuesto if not unicodedata.combining(c))
    return ' '.join(sin_acentos.lower().split())


class FormsEquipo(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre', 'imagen', 'pais', 'ciudad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Real Madrid Club de Fútbol'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pais': forms.Select(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Madrid'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre_norm = normalizar_texto(nombre)
            qs = Equipo.objects.all()
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            for eq in qs:
                if normalizar_texto(eq.nombre) == nombre_norm:
                    raise forms.ValidationError(
                        f"¡Club duplicado! Ya existe un equipo registrado con el nombre '{eq.nombre}'."
                    )
        return nombre


class FormsJugador(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = ['nombre', 'imagen', 'pais_nacimiento', 'posicion', 'activo', 'descripcion', 'equipo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Lamine Yamal'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pais_nacimiento': forms.Select(attrs={'class': 'form-control'}),
            'posicion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Extremo Derecho'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción y trayectoria...'}),
            'equipo': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        equipo = cleaned_data.get('equipo')
        pais = cleaned_data.get('pais_nacimiento')

        if nombre:
            nombre_norm = normalizar_texto(nombre)
            qs = Jugador.objects.all()
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            for j in qs.select_related('equipo', 'pais_nacimiento'):
                if normalizar_texto(j.nombre) == nombre_norm:
                    if equipo and j.equipo_id == equipo.pk:
                        self.add_error(
                            'nombre',
                            f"¡Jugador repetido! Ya existe '{j.nombre}' en el plantel de {equipo.nombre}."
                        )
                        break
                    elif pais and j.pais_nacimiento_id == pais.pk:
                        club_nombre = j.equipo.nombre if j.equipo else "Sin club asignado"
                        self.add_error(
                            'nombre',
                            f"¡Futbolista ya registrado! '{j.nombre}' ({pais.nombre}) ya figura en el sistema en el club '{club_nombre}'. No se puede registrar repetido."
                        )
                        break
                    else:
                        club_nombre = j.equipo.nombre if j.equipo else "Sin club asignado"
                        self.add_error(
                            'nombre',
                            f"Ya existe un futbolista registrado como '{j.nombre}' en el club '{club_nombre}'."
                        )
                        break

        return cleaned_data


class FormsPais(forms.ModelForm):
    class Meta:
        model = Pais
        fields = ['nombre', 'imagen', 'continente']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Argentina'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'continente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. América del Sur'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre_norm = normalizar_texto(nombre)
            qs = Pais.objects.all()
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            for p in qs:
                if normalizar_texto(p.nombre) == nombre_norm:
                    raise forms.ValidationError(
                        f"¡País duplicado! Ya existe '{p.nombre}' registrado en el sistema."
                    )
        return nombre
