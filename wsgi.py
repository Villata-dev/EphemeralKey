"""
Punto de entrada WSGI para despliegues en servidores de produccion (Gunicorn/uWSGI).
"""
from app import app
from core.logger import get_ephemeral_logger

log = get_ephemeral_logger("WSGI_ENTRY")
log.info("Inicializando EphemeralKey Web Suite en entorno de produccion.")

if __name__ == "__main__":
    app.run()
