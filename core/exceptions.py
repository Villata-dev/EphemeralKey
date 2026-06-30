class EphemeralError(Exception):
    """Clase base para excepciones de EphemeralKey"""
    pass

class NetworkTimeoutError(EphemeralError):
    """Lanzada cuando las APIs externas no responden"""
    pass

class CryptographyError(EphemeralError):
    """Lanzada en fallos de generacion de entropia"""
    pass
