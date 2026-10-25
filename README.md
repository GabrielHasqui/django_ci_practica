# Práctica CI: Django + PostgreSQL

Proyecto básico para la práctica de Gestión de la Configuración de Software.
Incluye `manage.py`, `project/`, una app funcional `app/`, PostgreSQL,
`requirements.txt`, migraciones y 16 pruebas automatizadas.

La aplicación permite crear, listar, editar, completar, reabrir y eliminar tareas.
Tiene validación de formularios, protección CSRF y registro del modelo en el admin.
Es una aplicación local de práctica, sin cuentas de usuario para la lista de tareas.

## Preparación en Windows

Requisitos: Python 3.10 o posterior compatible con Django 5.2, PostgreSQL instalado y Git.
Los comandos se ejecutan desde esta carpeta, donde está `manage.py`.

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/local_db.py start
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py runserver
```

Abre http://127.0.0.1:8000/ en el navegador. Detén el servidor con Ctrl+C.
Usar el ejecutable del entorno virtual evita tener que cambiar la política de PowerShell.

## Volver a abrir el proyecto

Si el entorno virtual y las dependencias ya están preparados:

```powershell
.\.venv\Scripts\python.exe scripts/local_db.py start
.\.venv\Scripts\python.exe manage.py runserver
```

## PostgreSQL

`scripts/local_db.py start` genera `.env` con claves aleatorias si todavía no existe.
Inicializa una instancia local propia dentro de `.local/postgres/`, en el puerto
`55432`, y crea la base `practica_ci`. No necesita la contraseña del servicio de
PostgreSQL que ya esté instalado en el equipo. El usuario local de esta instancia
tiene permisos para crear la base temporal de pruebas.

El script encuentra PostgreSQL en `PATH` o en `C:/Program Files/PostgreSQL/*/bin`.
Para otra ubicación, configura `PG_BIN` en `.env`.

```powershell
.\.venv\Scripts\python.exe scripts/local_db.py status
.\.venv\Scripts\python.exe scripts/local_db.py stop
```

Detener la instancia conserva las tareas. Los datos de la práctica están en
`.local/postgres/`; no borres esa carpeta si quieres conservarlos.

También puedes usar una base PostgreSQL que ya tengas: copia `.env.example` a
`.env`, cambia sus valores y ejecuta `manage.py migrate` sin utilizar el script
de base local. El usuario necesita permiso `CREATEDB` para `manage.py test`.
La conexión siempre usa PostgreSQL; no se sustituye por SQLite.

## Pruebas para la sesión 1

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test --verbosity 2
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Las pruebas verifican el motor PostgreSQL, creación y representación del modelo,
listado y contadores, estado vacío, validaciones, edición, cambio de estado,
eliminación, respuestas 404/405, escape de HTML y protección CSRF.
Se ejecutan en una base temporal `test_practica_ci`, que Django elimina al terminar;
las tareas de la aplicación no se usan para los tests.

En GitHub Actions se deberán instalar las dependencias, levantar un servicio
PostgreSQL y definir `DJANGO_SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`,
`DB_HOST` y `DB_PORT` antes de ejecutar `python manage.py test`.
Este proyecto deja preparada la aplicación base; el archivo de Actions corresponde
al siguiente paso de la sesión 1. Docker corresponde a la sesión 2.

## Administrador (opcional)

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Luego visita http://127.0.0.1:8000/admin/. No se incluye un usuario o contraseña
predeterminados.

## Archivos principales

```text
manage.py
requirements.txt
.env.example
project/                 Configuración, URLs, WSGI y ASGI
app/                     Modelo, formulario, vistas, URLs, admin y pruebas
  migrations/            Esquema de la base de datos
  templates/app/         Pantallas HTML
  static/app/            Estilos
scripts/local_db.py      Inicio y parada del PostgreSQL local
```

`.env`, `.venv/` y `.local/` están excluidos de Git. Las credenciales locales y los
datos de PostgreSQL no deben subirse al repositorio.

Referencia de compatibilidad: https://docs.djangoproject.com/en/5.2/faq/install/
