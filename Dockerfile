# Usa una imagen oficial de Python ligera
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia primero los requerimientos para aprovechar el caché de capas de Docker
COPY requirements.txt .

# Instala las dependencias y gunicorn (servidor de producción)
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copia el resto del código fuente
COPY . .

# Expone el puerto donde correrá el servidor
EXPOSE 5000

# Comando de ejecución usando Gunicorn en lugar del servidor de desarrollo de Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]