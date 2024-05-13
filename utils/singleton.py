import threading
from typing import Optional


class Singleton(type):
    _instance: Optional['Singleton'] = None
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs) -> 'Singleton':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
