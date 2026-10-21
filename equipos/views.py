from django.shortcuts import render
from .models import Equipo

def lista_equipos(request):
    # Trae los equipos junto con sus jugadores para optimizar consultas
    equipos = Equipo.objects.prefetch_related('jugadores').all()
    return render(request, 'equipos/index.html', {'equipos': equipos})