from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Equipo, Jugador, Pais
from .forms import FormsEquipo, FormsJugador, FormsPais


def lista_equipos(request):
    equipos = Equipo.objects.select_related('pais').prefetch_related('jugadores__pais_nacimiento').all()
    total_equipos = equipos.count()
    total_jugadores = Jugador.objects.count()
    total_paises = Pais.objects.count()
    return render(request, 'equipos/index.html', {
        'equipos': equipos,
        'total_equipos': total_equipos,
        'total_jugadores': total_jugadores,
        'total_paises': total_paises,
    })


def lista_paises(request):
    paises = Pais.objects.prefetch_related('jugadores__equipo').all()
    total_equipos = Equipo.objects.count()
    total_jugadores = Jugador.objects.count()
    total_paises = paises.count()
    return render(request, 'equipos/paises.html', {
        'paises': paises,
        'total_equipos': total_equipos,
        'total_jugadores': total_jugadores,
        'total_paises': total_paises,
    })


def lista_jugadores(request):
    jugadores = Jugador.objects.select_related('equipo', 'pais_nacimiento').all()
    total_equipos = Equipo.objects.count()
    total_jugadores = jugadores.count()
    total_paises = Pais.objects.count()
    return render(request, 'equipos/jugadores.html', {
        'jugadores': jugadores,
        'total_equipos': total_equipos,
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

def editar_equipo(request, codigo_equipo):
    equipo = get_object_or_404(Equipo, codigo_equipo=codigo_equipo)
    form = FormsEquipo(request.POST or None, request.FILES or None, instance=equipo)
    if 'codigo_equipo' in form.fields:
        form.fields['codigo_equipo'].disabled = True

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Club "{equipo.nombre}" actualizado correctamente')
        return redirect('lista_equipos')

    return render(request, 'equipos/editar_equipo.html', {
        'form': form,
        'equipo': equipo,
        'titulo': f'Editar Equipo: {equipo.nombre}'
    })


def editar_jugador(request, jugador_id):
    jugador = get_object_or_404(Jugador, pk=jugador_id)
    form = FormsJugador(request.POST or None, request.FILES or None, instance=jugador)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Futbolista "{jugador.nombre}" actualizado correctamente')
        return redirect('lista_jugadores')

    return render(request, 'equipos/editar_jugador.html', {
        'form': form,
        'jugador': jugador,
        'titulo': f'Editar Jugador: {jugador.nombre}'
    })


def editar_pais(request, pais_id):
    pais = get_object_or_404(Pais, pk=pais_id)
    form = FormsPais(request.POST or None, request.FILES or None, instance=pais)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'País "{pais.nombre}" actualizado correctamente')
        return redirect('lista_paises')

    return render(request, 'equipos/editar_pais.html', {
        'form': form,
        'pais': pais,
        'titulo': f'Editar País: {pais.nombre}'
    })


def eliminar_equipo(request, codigo_equipo):
    equipo = get_object_or_404(Equipo, codigo_equipo=codigo_equipo)
    if request.method == 'POST':
        nombre = equipo.nombre
        equipo.delete()
        messages.success(request, f'Club "{nombre}" eliminado correctamente.')
        return redirect('lista_equipos')

    return render(request, 'equipos/eliminar_equipo.html', {
        'equipo': equipo,
        'total_jugadores': equipo.jugadores.count(),
        'jugadores': equipo.jugadores.all()[:6]
    })


def eliminar_jugador(request, jugador_id):
    jugador = get_object_or_404(Jugador, pk=jugador_id)
    if request.method == 'POST':
        nombre = jugador.nombre
        jugador.delete()
        messages.success(request, f'Futbolista "{nombre}" eliminado correctamente.')
        return redirect('lista_jugadores')

    return render(request, 'equipos/eliminar_jugador.html', {
        'jugador': jugador
    })


def eliminar_pais(request, pais_id):
    pais = get_object_or_404(Pais, pk=pais_id)
    if request.method == 'POST':
        nombre = pais.nombre
        pais.delete()
        messages.success(request, f'País "{nombre}" eliminado correctamente.')
        return redirect('lista_paises')

    return render(request, 'equipos/eliminar_pais.html', {
        'pais': pais,
        'total_equipos': pais.equipos.count(),
        'total_jugadores': pais.jugadores.count()
    })