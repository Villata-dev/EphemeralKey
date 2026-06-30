import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_secure_session() -> requests.Session:
    """Configura una sesion HTTP con estrategia de reintentos exponenciales (Backoff)"""
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
