#!/bin/sh
set -e

# Aplicar las migraciones una vez que PostgreSQL este disponible.
python manage.py migrate --noinput

# Ejecutar el comando principal indicado por el Dockerfile.
exec "$@"
