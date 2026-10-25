# Práctica de integración y despliegue continuo

Proyecto académico de Gestión de la Configuración de Software para aplicar un flujo CI/CD sobre una aplicación Django con PostgreSQL.

La aplicación permite crear, editar, completar y eliminar tareas, e incluye 16 pruebas automatizadas.

## Desarrollo de la práctica

1. Preparación del entorno e integración continua con GitHub Actions.
2. Automatización de la construcción con Docker.
3. Simulación del despliegue con Docker Compose.
4. Validación del pipeline y documentación de resultados.

Actualmente, el proyecto cuenta con pruebas automáticas en GitHub Actions. La construcción y el despliegue con Docker corresponden a las siguientes sesiones.

## Ejecución local

Con el entorno virtual activado, las dependencias de `requirements.txt` instaladas y PostgreSQL configurado en `.env` a partir de `.env.example`, ejecuta:

```bash
python manage.py migrate
python manage.py runserver
```

La aplicación se abre en http://127.0.0.1:8000/. Para ejecutar las pruebas:

```bash
python manage.py test
```
