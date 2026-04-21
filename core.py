import secrets
import string
import requests

def generate_password(length=18):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def get_temp_email():
    # Genera un correo aleatorio usando 1secmail
    response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
    if response.status_code == 200:
        return response.json()[0]
    return "Error al generar correo"

def check_inbox(email):
    # Revisa los mensajes (ejemplo: 'usuario@1secmail.com')
    user, domain = email.split('@')
    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={user}&domain={domain}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []