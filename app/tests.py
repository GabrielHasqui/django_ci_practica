from django.db import connection
from django.test import Client, TestCase
from django.urls import reverse

from .models import Tarea


class TareaTests(TestCase):
    def setUp(self):
        self.tarea = Tarea.objects.create(titulo="Preparar entorno", descripcion="Instalar dependencias")

    def test_base_de_datos_es_postgresql(self):
        self.assertEqual(connection.vendor, "postgresql")

    def test_tarea_nueva_esta_pendiente(self):
        self.assertFalse(self.tarea.completada)
        self.assertEqual(str(self.tarea), "Preparar entorno")

    def test_lista_muestra_tareas_y_resumen(self):
        response = self.client.get(reverse("tareas:lista"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Preparar entorno")
        self.assertEqual(response.context["total"], 1)
        self.assertEqual(response.context["pendientes"], 1)
        self.assertEqual(response.context["completadas"], 0)

    def test_lista_vacia(self):
        Tarea.objects.all().delete()
        response = self.client.get(reverse("tareas:lista"))
        self.assertContains(response, "Tu lista está lista para empezar")

    def test_crear_tarea(self):
        response = self.client.post(reverse("tareas:lista"), {"titulo": "Escribir tests", "descripcion": "Probar el modelo"})
        self.assertRedirects(response, reverse("tareas:lista"))
        self.assertTrue(Tarea.objects.filter(titulo="Escribir tests").exists())

    def test_rechazar_titulo_vacio(self):
        for titulo in ("", "   "):
            with self.subTest(titulo=titulo):
                response = self.client.post(reverse("tareas:lista"), {"titulo": titulo})
                self.assertTrue(response.context["form"].errors)
        self.assertEqual(Tarea.objects.count(), 1)

    def test_rechazar_titulo_demasiado_largo(self):
        response = self.client.post(reverse("tareas:lista"), {"titulo": "a" * 121})
        self.assertIn("titulo", response.context["form"].errors)
        self.assertEqual(Tarea.objects.count(), 1)

    def test_abrir_formulario_edicion(self):
        response = self.client.get(reverse("tareas:editar", args=[self.tarea.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Preparar entorno")

    def test_editar_tarea(self):
        response = self.client.post(reverse("tareas:editar", args=[self.tarea.pk]), {"titulo": "Entorno listo", "descripcion": "Verificado"})
        self.assertRedirects(response, reverse("tareas:lista"))
        self.tarea.refresh_from_db()
        self.assertEqual(self.tarea.titulo, "Entorno listo")
        self.assertEqual(self.tarea.descripcion, "Verificado")

    def test_edicion_invalida_preserva_tarea(self):
        response = self.client.post(reverse("tareas:editar", args=[self.tarea.pk]), {"titulo": ""})
        self.assertIn("titulo", response.context["form"].errors)
        self.tarea.refresh_from_db()
        self.assertEqual(self.tarea.titulo, "Preparar entorno")

    def test_completar_y_reabrir(self):
        url = reverse("tareas:estado", args=[self.tarea.pk])
        for esperado in (True, False):
            response = self.client.post(url)
            self.assertRedirects(response, reverse("tareas:lista"))
            self.tarea.refresh_from_db()
            self.assertEqual(self.tarea.completada, esperado)

    def test_eliminar_tarea(self):
        response = self.client.post(reverse("tareas:eliminar", args=[self.tarea.pk]))
        self.assertRedirects(response, reverse("tareas:lista"))
        self.assertFalse(Tarea.objects.filter(pk=self.tarea.pk).exists())

    def test_get_no_modifica_ni_elimina(self):
        for accion in ("estado", "eliminar"):
            response = self.client.get(reverse(f"tareas:{accion}", args=[self.tarea.pk]))
            self.assertEqual(response.status_code, 405)
        self.tarea.refresh_from_db()
        self.assertFalse(self.tarea.completada)

    def test_tarea_inexistente_devuelve_404(self):
        for accion in ("editar", "estado", "eliminar"):
            response = self.client.post(reverse(f"tareas:{accion}", args=[999999]), {"titulo": "No existe"})
            self.assertEqual(response.status_code, 404)

    def test_titulo_html_se_muestra_como_texto(self):
        Tarea.objects.create(titulo="<script>alert('hola')</script>")
        response = self.client.get(reverse("tareas:lista"))
        self.assertContains(response, "&lt;script&gt;")
        self.assertNotContains(response, "<script>alert")

    def test_post_requiere_csrf(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse("tareas:lista"), {"titulo": "Sin token"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Tarea.objects.count(), 1)
