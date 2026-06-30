import time
from functools import wraps
from flask import request
from core.logger import get_ephemeral_logger

log = get_ephemeral_logger("API_METRICS")

def measure_execution_time(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        duration = (time.time() - start) * 1000
        log.info(f"Endpoint {request.endpoint} executado en {duration:.2f}ms")
        return result
    return decorated_function
