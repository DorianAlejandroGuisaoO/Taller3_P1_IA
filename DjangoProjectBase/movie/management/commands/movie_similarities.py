import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from sentence_transformers import SentenceTransformer

class Command(BaseCommand):
    help = "Compare two movies and optionally a prompt using local embeddings (sentence-transformers)"

    def handle(self, *args, **kwargs):
        # ✅ Carga el modelo local (solo la primera vez lo descarga)
        model = SentenceTransformer("all-MiniLM-L6-v2")

        def get_embedding(text):
            return model.encode(text)

        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        # ✅ Cambia estos títulos según los que tengas en tu DB
        movie1 = Movie.objects.get(title="Carmencita")
        movie2 = Movie.objects.get(title="Cinderella")

        # ✅ Embeddings de las descripciones
        emb1 = get_embedding(movie1.description)
        emb2 = get_embedding(movie2.description)

        similarity = cosine_similarity(emb1, emb2)
        self.stdout.write(f"🎬 Similaridad entre '{movie1.title}' y '{movie2.title}': {similarity:.4f}")

        # ✅ Comparar contra un prompt opcional
        prompt = "pelicula sobre drama romantico"
        prompt_emb = get_embedding(prompt)

        sim_prompt_movie1 = cosine_similarity(prompt_emb, emb1)
        sim_prompt_movie2 = cosine_similarity(prompt_emb, emb2)

        self.stdout.write(f"📝 Similitud prompt vs '{movie1.title}': {sim_prompt_movie1:.4f}")
        self.stdout.write(f"📝 Similitud prompt vs '{movie2.title}': {sim_prompt_movie2:.4f}")
