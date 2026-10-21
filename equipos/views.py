from django.shortcuts import render
from .models import Equipo

def lista_equipos(request):
    # Trae los equipos junto con sus países y jugadores con sus países de nacimiento para optimizar consultas
    equipos = Equipo.objects.select_related('pais').prefetch_related('jugadores__pais_nacimiento').all()
    return render(request, 'equipos/index.html', {'equipos': equipos})
