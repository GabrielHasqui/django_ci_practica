# Notas de Despliegue - Sesión 3

## Requisitos
- Tener Docker y Docker Compose instalados y ejecutándose.

## Pasos para desplegar en un entorno nuevo
1. Descargar el artefacto `artefacto-docker.zip` desde la pestaña Actions de GitHub.
2. Descomprimir el archivo `.zip` para obtener el archivo `imagen-django.tar`.
3. Copiar el archivo `docker-compose.yml` original y colocarlo en la misma carpeta junto al `.tar`.
4. Cargar la imagen descargada a Docker ejecutando en la terminal: `docker load -i imagen-django.tar`
5. Levantar los servicios ejecutando: `docker compose up -d`
6. Acceder a la aplicación desde el navegador web en `http://localhost:8000`