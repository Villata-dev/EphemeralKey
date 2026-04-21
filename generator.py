import secrets
import string

def generate_secure_password(length=16, use_special=True):
    alphabet = string.ascii_letters + string.digits
    if use_special:
        alphabet += string.punctuation
    
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

# Ejemplo de uso
print(f"Tu llave efímera: {generate_secure_password()}")