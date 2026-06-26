from flask import Flask, render_template, jsonify, request
import secrets
import string
import requests

app = Flask(__name__)

# --- RUTAS DE LA INTERFAZ ---

@app.route('/')
def index():
    return render_template('index.html')

# --- RUTAS DE LA API REST (BACKEND) ---

@app.route('/api/password')
def get_password():
    length = int(request.args.get('length', 18))
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(chars) for _ in range(length))
    return jsonify({'password': password})

@app.route('/api/email/new')
def new_email():
    try:
        r = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1", timeout=5)
        if r.status_code == 200:
            return jsonify({'email': r.json()[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'No se pudo contactar a la API'}), 500

@app.route('/api/email/check')
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
        return jsonify({'error': 'No se pudo leer el mensaje'})

if __name__ == '__main__':
    # Ejecuta el servidor en el puerto 5000 por defecto
    app.run(debug=True, host='0.0.0.0', port=5000)