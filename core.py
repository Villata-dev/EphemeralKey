import secrets
import string

def generate_password(length=18, level='high'):
    characters = string.ascii_letters + string.digits
    if level == 'high':
        characters += string.punctuation
    
    return ''.join(secrets.choice(characters) for _ in range(length))

# Aquí luego añadiremos la función para conectar con la API de correos  