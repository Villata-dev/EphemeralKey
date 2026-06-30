import hashlib
from .network import get_secure_session

def check_password_breach(password: str) -> int:
    """Implementa k-Anonymity usando SHA-1 contra HIBP API para verificar filtraciones"""
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    
    session = get_secure_session()
    response = session.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    
    if response.status_code == 200:
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return int(count)
    return 0
