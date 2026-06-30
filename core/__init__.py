"""
EphemeralKey Core Library
Provee los modulos criptograficos, de red y de seguridad operativa.
"""
from .crypto import generate_complex_password
from .passphrase import generate_passphrase
from .pwned import check_password_breach
from .shredder import secure_delete

__all__ = [
    'generate_complex_password',
    'generate_passphrase',
    'check_password_breach',
    'secure_delete'
]
