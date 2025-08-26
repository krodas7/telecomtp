# Dockerfile para Sistema ARCA Construcción
# Multi-stage build para optimizar tamaño final

# Etapa 1: Build de dependencias
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Etapa 2: Imagen final
FROM python:3.11-slim

# Crear usuario no-root
RUN useradd --create-home --shell /bin/bash arca

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libpq5 \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Crear directorios necesarios
RUN mkdir -p /app /var/www/staticfiles /var/www/media /var/log

# Copiar dependencias instaladas
COPY --from=builder /root/.local /home/arca/.local

# Copiar código de la aplicación
COPY . /app/

# Cambiar permisos
RUN chown -R arca:arca /app /var/www /var/log

# Cambiar al usuario arca
USER arca
WORKDIR /app

# Configurar PATH
ENV PATH=/home/arca/.local/bin:$PATH

# Variables de entorno
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=sistema_construccion.settings

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "sistema_construccion.wsgi:application"]
