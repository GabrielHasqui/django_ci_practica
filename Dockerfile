# Sesion 2: imagen para la aplicacion Django del equipo.
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Se copian primero las dependencias para aprovechar la cache del build.
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copiar el codigo fuente de Django y el script de arranque.
COPY . .

# Normalizar los saltos de linea de Windows y permitir la ejecucion del script.
RUN sed -i 's/\r$//' /app/docker-entrypoint.sh && chmod +x /app/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
