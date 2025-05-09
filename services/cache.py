import time as time_module
from functools import wraps
import json

# In-memory cache with expiration
_cache = {}

def ttl_cache(ttl_seconds=86400):  # 86400 seconds = 24 hours
    def decorator(fn):
        @wraps(fn)
        def wrapped(*args):
            key = json.dumps(args, sort_keys=True)
            now = time_module.time()
            if key in _cache:
                result, timestamp = _cache[key]
                if now - timestamp < ttl_seconds:
                    return result
            result = fn(*args)
            _cache[key] = (result, now)
            return result
        return wrapped
    return decorator