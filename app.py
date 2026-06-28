from flask import Flask, render_template, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import secrets
import string
import requests
import logging

# Configuración de servidor de producción
app = Flask(__name__)

# --- CAPA DE SEGURIDAD: RATE LIMITING ---
# Previene ataques de denegación de servicio (DoS) y abuso de la API
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# --- CAPA DE SEGURIDAD: HTTP HEADERS ---
@app.after_request
def set_security_headers(response):
    """Inyecta cabeceras de seguridad estrictas en cada respuesta del servidor"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# --- RUTAS DE LA INTERFAZ ---

@app.route('/')
def index():
    return render_template('index.html')

# --- RUTAS DE LA API REST (BACKEND) ---

@app.route('/api/password')
@limiter.limit("10 per minute") # Límite estricto para generación de claves
def get_password():
    length = int(request.args.get('length', 24))
    # Forzar límite máximo de longitud por seguridad de memoria
    if length > 128: length = 128 
    
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(chars) for _ in range(length))
    return jsonify({'password': password})

@app.route('/api/email/new')
@limiter.limit("5 per minute") # Evitar ban de la API de 1secmail
def new_email():
    try:
        r = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1", timeout=5)
        if r.status_code == 200:
            return jsonify({'email': r.json()[0]})
    except Exception as e:
        logging.error(f"Error de conexión API: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    return jsonify({'error': 'Gateway Timeout'}), 504

@app.route('/api/email/check')
@limiter.exempt # Exento de rate limit estricto porque el frontend hace polling cada 10s
def check_email():
    email = request.args.get('email')
    if not email:
        return jsonify([])
    
    try:
        user, domain = email.split('@')
        r = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={user}&domain={domain}", timeout=5)
        return jsonify(r.json() if r.status_code == 200 else [])
    except Exception:
        return jsonify([])

@app.route('/api/email/read')
def read_email():
    email = request.args.get('email')
    mail_id = request.args.get('id')
    
    try:
        user, domain = email.split('@')
        r = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={user}&domain={domain}&id={mail_id}", timeout=5)
        return jsonify(r.json() if r.status_code == 200 else {})
    except Exception:
        return jsonify({'error': 'Cannot retrieve message payload'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)