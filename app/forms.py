from django import forms
from .models import Tarea


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ["titulo", "descripcion"]
        widgets = {
            "titulo": forms.TextInput(attrs={"placeholder": "Ej.: Preparar las pruebas"}),
            "descripcion": forms.Textarea(attrs={"rows": 3, "placeholder": "Detalles opcionales"}),
        }
