import threading

class ThreadSafeCounter():
    """
    A thread-safe counter class to keep track of the number of messages
    consumed by a consumer.
    """

    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()
    
    def get_and_increment(self, threshold: int) -> int:
        """Get the current value and increment it by 1 if it is less
        than the threshold."""
        with self._lock:
            current_value = self._value
            if self._value < threshold:
                self._value += 1
        return current_value
