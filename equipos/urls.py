from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_equipos, name='lista_equipos'),
    path('paises/', views.lista_paises, name='lista_paises'),
    path('jugadores/', views.lista_jugadores, name='lista_jugadores'),
    path('crear_equipo/', views.crear_equipo, name='crear_equipo'),
    path('crear_jugador/', views.crear_jugador, name='crear_jugador'),
    path('crear_pais/', views.crear_pais, name='crear_pais'),
]
