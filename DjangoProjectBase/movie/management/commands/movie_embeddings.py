import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from sentence_transformers import SentenceTransformer

class Command(BaseCommand):
    help = "Generate and store embeddings for all movies in the database (using sentence-transformers, local & free)"

    def handle(self, *args, **kwargs):
        # ✅ Cargar modelo local de embeddings (gratis)
        self.stdout.write("🔄 Loading sentence-transformers model (all-MiniLM-L6-v2)...")
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.stdout.write("👌 Model loaded successfully.")

        # ✅ Obtener todas las películas
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies in the database")

        # ✅ Función para generar embedding local
        def get_embedding(text):
            emb = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
            return np.array(emb, dtype=np.float32)

        # ✅ Generar y almacenar embeddings
        for movie in movies:
            try:
                emb = get_embedding(movie.description or movie.title)
                movie.emb = emb.tobytes()
                movie.save()
                self.stdout.write(self.style.SUCCESS(f"✅ Embedding stored for: {movie.title}"))
            except Exception as e:
                self.stderr.write(f"❌ Failed to generate embedding for {movie.title}: {e}")

        self.stdout.write(self.style.SUCCESS("🎯 Finished generating embeddings for all movies"))
