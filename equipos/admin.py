from django.contrib import admin
from .models import Equipo, Jugador, Pais

admin.site.register(Pais)
admin.site.register(Equipo)
admin.site.register(Jugador)