import time

class TimedCache:
    def __init__(self):
        self._cache = {}

    def set(self, key: int, ttl: int) -> None:
        expire_at = int(time.time()) + ttl
        self._cache[key] = expire_at

    def get(self, key: int) -> bool:
        current_time = int(time.time())
        if key in self._cache and self._cache[key] > current_time:
            return True
        self._cache.pop(key, None)
        return False

    def clean(self) -> None:
        current_time = int(time.time())
        self._cache = {k: v for k, v in self._cache.items() if v > current_time}