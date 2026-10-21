from django.db import models

class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='paises/', blank=True, null=True)
    continente = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    codigo_equipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='equipos/', blank=True, null=True)
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, blank=True, related_name='equipos')
    ciudad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='jugadores/', blank=True, null=True)
    pais_nacimiento = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, blank=True, related_name='jugadores')
    posicion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True, default='Sin descripción disponible.')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='jugadores')

    def __str__(self):
        return f"{self.nombre} ({self.posicion})"