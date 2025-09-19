import unicodedata
import re
from pathlib import Path

from django.core.management.base import BaseCommand
from movie.models import Movie


def normalizar_nombre(texto: str) -> str:
    """
    Convierte un título de película en un nombre seguro para buscar el archivo:
    - Minúsculas
    - Quita tildes y caracteres especiales
    - Sustituye espacios por '_'
    - Solo letras, números y '_'
    """
    # Quitar acentos / tildes
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = texto.lower().strip()

    texto = texto.replace(" ", "_")          # espacios → _
    texto = re.sub(r"[^a-z0-9_]", "", texto)  # eliminar símbolos raros
    return texto


class Command(BaseCommand):
    help = "Asigna a cada película su imagen desde media/movie/images/"

    def handle(self, *args, **options):
        # Carpeta donde están las imágenes
        carpeta = Path("media/movie/images")
        if not carpeta.exists():
            self.stderr.write(self.style.ERROR(f"No existe la carpeta: {carpeta.resolve()}"))
            return

        # Listar todos los archivos m_* en la carpeta
        archivos = list(carpeta.glob("m_*.*"))
        self.stdout.write(f"Se encontraron {len(archivos)} archivos de imagen.\n")

        ok = 0
        sin_img = []

        for movie in Movie.objects.all():
            titulo_norm = normalizar_nombre(movie.title)
            patron = f"m_{titulo_norm}"

            # Buscar archivo que contenga el patrón (ignora mayúsculas y acentos)
            archivo = next(
                (
                    a
                    for a in archivos
                    if normalizar_nombre(a.stem) == patron
                ),
                None,
            )

            if archivo:
                # Actualizar campo image (ruta relativa desde media/)
                movie.image = f"movie/images/{archivo.name}"
                movie.save()
                self.stdout.write(self.style.SUCCESS(f"[OK] {movie.title} → {archivo}"))
                ok += 1
            else:
                self.stdout.write(f"[NO IMG] No se encontró imagen para: {movie.title}")
                sin_img.append(movie.title)

        self.stdout.write(self.style.SUCCESS(f"\n✔ Actualizadas {ok} películas con su imagen."))
        if sin_img:
            self.stdout.write("\nPelículas sin imagen:")
            for t in sin_img:
                self.stdout.write(f" - {t}")
