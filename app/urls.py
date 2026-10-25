from django.urls import path
from . import views

app_name = "tareas"
urlpatterns = [
    path("", views.lista, name="lista"),
    path("tareas/<int:pk>/editar/", views.editar, name="editar"),
    path("tareas/<int:pk>/estado/", views.cambiar_estado, name="estado"),
    path("tareas/<int:pk>/eliminar/", views.eliminar, name="eliminar"),
]
