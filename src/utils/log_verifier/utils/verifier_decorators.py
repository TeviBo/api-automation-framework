import time
from functools import wraps


def retry_decorator(max_retries=20, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                log_entry = func(*args, **kwargs)
                if log_entry:
                    return log_entry
                time.sleep(delay)
                retries += 1
            return []

        return wrapper

    return decorator
