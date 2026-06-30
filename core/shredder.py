import os
import secrets

def secure_delete(filepath: str, passes: int = 3):
    """Sobrescribe un archivo con bytes aleatorios antes de eliminarlo del disco"""
    if not os.path.exists(filepath): return
    length = os.path.getsize(filepath)
    with open(filepath, "ba+", buffering=0) as f:
        for _ in range(passes):
            f.seek(0)
            f.write(secrets.token_bytes(length))
    os.remove(filepath)
