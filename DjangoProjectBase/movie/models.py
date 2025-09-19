from django.db import models
import numpy as np

def get_default_array():
    # Modelo all-MiniLM-L6-v2 produce vectores de 384 dimensiones
    default_arr = np.zeros(384, dtype=np.float32)
    return default_arr.tobytes()

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)
    image = models.ImageField(upload_to='movie/images/', default='movie/images/default.jpg')
    url = models.URLField(blank=True)
    genre = models.CharField(blank=True, max_length=250)
    year = models.IntegerField(blank=True, null=True)

    # Guardamos el embedding en binario (vector de 384 floats)
    emb = models.BinaryField(default=get_default_array, blank=True)

    def __str__(self):
        return self.title
