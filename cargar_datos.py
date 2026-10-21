import os

import django
import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from equipos.models import Equipo, Jugador

# Solo se usan para relacionar cada jugador con un equipo ya existente en BD.
# No se crean ni actualizan países ni equipos.
JUGADORES_ACTUALIZAR = [
    {
        'equipo': 'Fútbol Club Barcelona',
        'nombre': 'Lamine Yamal',
        'imagen': 'https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Fútbol Club Barcelona',
        'nombre': 'Raphinha',
        'imagen': 'https://images.unsplash.com/photo-1521417531038-92841cc7d2f8?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Fútbol Club Barcelona',
        'nombre': 'Pedri',
        'imagen': 'https://images.unsplash.com/photo-1547347298-4074fc3086f0?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Fútbol Club Barcelona',
        'nombre': 'Robert Lewandowski',
        'imagen': 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Club Atlético de Madrid',
        'nombre': 'Antoine Griezmann',
        'imagen': 'https://images.unsplash.com/photo-1556056504-5c7696c4c28d?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Club Atlético de Madrid',
        'nombre': 'Jan Oblak',
        'imagen': 'https://images.unsplash.com/photo-1517466787929-bc90951d0974?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Club Atlético de Madrid',
        'nombre': 'Julián Álvarez',
        'imagen': 'https://images.unsplash.com/photo-1534158914592-062992fbe900?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Club Atlético de Madrid',
        'nombre': 'Rodrigo De Paul',
        'imagen': 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Real Madrid Club de Fútbol',
        'nombre': 'Vinícius Júnior',
        'imagen': 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Real Madrid Club de Fútbol',
        'nombre': 'Kylian Mbappé',
        'imagen': 'https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Real Madrid Club de Fútbol',
        'nombre': 'Jude Bellingham',
        'imagen': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Real Madrid Club de Fútbol',
        'nombre': 'Federico Valverde',
        'imagen': 'https://images.unsplash.com/photo-1518604666860-9ed391f76460?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Real Madrid Club de Fútbol',
        'nombre': 'Thibaut Courtois',
        'imagen': 'https://images.unsplash.com/photo-1543351611-58f69d7c1781?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Manchester City Football Club',
        'nombre': 'Erling Haaland',
        'imagen': 'https://images.unsplash.com/photo-1560272564-c1b1d49d44a3?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Manchester City Football Club',
        'nombre': 'Kevin De Bruyne',
        'imagen': 'https://images.unsplash.com/photo-1511884642898-4c92249e20b6?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Manchester City Football Club',
        'nombre': 'Rodri',
        'imagen': 'https://images.unsplash.com/photo-1529900748604-1b4aa95a8f7a?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Manchester City Football Club',
        'nombre': 'Phil Foden',
        'imagen': 'https://images.unsplash.com/photo-1579952363873-27d3bfad9c0d?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Liverpool Football Club',
        'nombre': 'Mohamed Salah',
        'imagen': 'https://images.unsplash.com/photo-1517466787929-bc90951d0974?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Liverpool Football Club',
        'nombre': 'Luis Díaz',
        'imagen': 'https://images.unsplash.com/photo-1521417531038-92841cc7d2f8?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Liverpool Football Club',
        'nombre': 'Alexis Mac Allister',
        'imagen': 'https://images.unsplash.com/photo-1547347298-4074fc3086f0?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Liverpool Football Club',
        'nombre': 'Virgil van Dijk',
        'imagen': 'https://images.unsplash.com/photo-1556056504-5c7696c4c28d?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Paris Saint-Germain Football Club',
        'nombre': 'Ousmane Dembélé',
        'imagen': 'https://images.unsplash.com/photo-1534158914592-062992fbe900?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Paris Saint-Germain Football Club',
        'nombre': 'Achraf Hakimi',
        'imagen': 'https://images.unsplash.com/photo-1579952363873-27d3bfad9c0d?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Paris Saint-Germain Football Club',
        'nombre': 'Gianluigi Donnarumma',
        'imagen': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Paris Saint-Germain Football Club',
        'nombre': 'Désiré Doué',
        'imagen': 'https://images.unsplash.com/photo-1560272564-c1b1d49d44a3?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Fußball-Club Bayern München',
        'nombre': 'Harry Kane',
        'imagen': 'https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Fußball-Club Bayern München',
        'nombre': 'Jamal Musiala',
        'imagen': 'https://images.unsplash.com/photo-1511884642898-4c92249e20b6?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Fußball-Club Bayern München',
        'nombre': 'Alphonso Davies',
        'imagen': 'https://images.unsplash.com/photo-1529900748604-1b4aa95a8f7a?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Fußball-Club Bayern München',
        'nombre': 'Joshua Kimmich',
        'imagen': 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Football Club Internazionale Milano',
        'nombre': 'Lautaro Martínez',
        'imagen': 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Football Club Internazionale Milano',
        'nombre': 'Nicolò Barella',
        'imagen': 'https://images.unsplash.com/photo-1518604666860-9ed391f76460?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Football Club Internazionale Milano',
        'nombre': 'Hakan Çalhanoğlu',
        'imagen': 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=900&q=80',
    },
    {
        'equipo': 'Football Club Internazionale Milano',
        'nombre': 'Yann Sommer',
        'imagen': 'https://images.unsplash.com/photo-1543351611-58f69d7c1781?auto=format&fit=crop&w=900&q=80',
    },
]


def guardar_imagen_jugador(jugador, url):
    if not url or not jugador:
        return False

    try:
        respuesta = requests.get(
            url,
            timeout=25,
            stream=True,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'},
        )
        respuesta.raise_for_status()

        content_type = respuesta.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            raise ValueError(f'La URL no devuelve una imagen válida: {url}')

        extension = '.jpg'
        mime = content_type.split('/')[-1].lower()
        if mime in {'png', 'webp', 'jpeg', 'gif'}:
            extension = f'.{mime if mime != "jpeg" else "jpg"}'

        nombre_fichero = f'{slugify(jugador.nombre)}_jugador{extension}'
        jugador.imagen.save(nombre_fichero, ContentFile(respuesta.content), save=True)
        print(f'   -> Imagen guardada para {jugador.nombre}: {nombre_fichero}')
        return True
    except Exception as exc:
        print(f'   -> No se pudo guardar la imagen para {jugador.nombre}: {exc}')
        return False


def poblar_imagenes_jugadores():
    print('==================================================')
    print(' SUBIENDO IMÁGENES SOLO A JUGADORES EXISTENTES')
    print('==================================================')

    total = 0

    for item in JUGADORES_ACTUALIZAR:
        equipo = Equipo.objects.filter(nombre=item['equipo']).first()
        if not equipo:
            print(f'[!] No existe el equipo: {item["equipo"]}')
            continue

        jugador = Jugador.objects.filter(nombre=item['nombre'], equipo=equipo).first()
        if not jugador:
            print(f'[!] No existe el jugador: {item["nombre"]} en {equipo.nombre}')
            continue

        if guardar_imagen_jugador(jugador, item['imagen']):
            total += 1

    print('==================================================')
    print(f' ¡Listo! Se actualizaron {total} imágenes de jugadores.')
    print('==================================================')


if __name__ == '__main__':
    poblar_imagenes_jugadores()