from django.db import models


class Tarea(models.Model):
    titulo = models.CharField("Título", max_length=120)
    descripcion = models.TextField("Descripción", blank=True)
    completada = models.BooleanField("Completada", default=False)
    creada_en = models.DateTimeField("Fecha de creación", auto_now_add=True)

    class Meta:
        ordering = ["completada", "-creada_en", "-pk"]
        verbose_name = "tarea"
        verbose_name_plural = "tareas"

    def __str__(self):
        return self.titulo
