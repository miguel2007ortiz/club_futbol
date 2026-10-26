from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Equipo, Jugador, Pais
from .forms import FormsEquipo, FormsJugador, FormsPais


def lista_equipos(request):
    equipos = Equipo.objects.select_related('pais').prefetch_related('jugadores__pais_nacimiento').all()
    total_jugadores = Jugador.objects.count()
    total_paises = Pais.objects.count()
    return render(request, 'equipos/index.html', {
        'equipos': equipos,
        'total_jugadores': total_jugadores,
        'total_paises': total_paises,
    })


def crear_equipo(request):
    form = FormsEquipo(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Equipo creado correctamente')
        return redirect('lista_equipos')

    return render(request, 'equipos/crear_equipo.html', {'form': form})


def crear_jugador(request):
    form = FormsJugador(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Jugador creado correctamente')
        return redirect('lista_equipos')

    return render(request, 'equipos/crear_jugador.html', {'form': form})


def crear_pais(request):
    form = FormsPais(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'País creado correctamente')
        return redirect('lista_equipos')

    return render(request, 'equipos/crear_pais.html', {'form': form})
