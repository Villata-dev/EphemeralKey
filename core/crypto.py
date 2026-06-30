import secrets
import string

def generate_complex_password(length: int = 24, exclude_ambiguous: bool = True) -> str:
    """Genera contrasenas evitando caracteres ambiguos como l, 1, O, 0"""
    chars = string.ascii_letters + string.digits + string.punctuation
    if exclude_ambiguous:
        chars = chars.translate(str.maketrans('', '', 'l1O0I'))
    return ''.join(secrets.choice(chars) for _ in range(length))
