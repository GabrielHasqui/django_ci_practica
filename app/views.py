from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import TareaForm
from .models import Tarea


@require_http_methods(["GET", "POST"])
def lista(request):
    form = TareaForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Tarea creada correctamente.")
        return redirect("tareas:lista")
    tareas = Tarea.objects.all()
    return render(request, "app/lista.html", {
        "form": form,
        "tareas": tareas,
        "total": tareas.count(),
        "pendientes": tareas.filter(completada=False).count(),
        "completadas": tareas.filter(completada=True).count(),
    })


@require_http_methods(["GET", "POST"])
def editar(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    form = TareaForm(request.POST if request.method == "POST" else None, instance=tarea)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Tarea actualizada.")
        return redirect("tareas:lista")
    return render(request, "app/editar.html", {"form": form, "tarea": tarea})


@require_POST
def cambiar_estado(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    tarea.completada = not tarea.completada
    tarea.save(update_fields=["completada"])
    return redirect("tareas:lista")


@require_POST
def eliminar(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    tarea.delete()
    messages.success(request, "Tarea eliminada.")
    return redirect("tareas:lista")
