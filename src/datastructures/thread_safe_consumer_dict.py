import threading
from typing import Dict

from src.datastructures.thread_safe_counter import ThreadSafeCounter


class ThreadSafeConsumerDict:
    """
    A thread-safe dictionary class to store the mapping of consumer ids
    with their offsets in the queue.

    Note: It is the users responsibility to ensure that the key being
    passed to the get_and_increment method is present in the dictionary.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._dict: Dict[str, ThreadSafeCounter] = {}

    def add(self, consumer_id: str) -> None:
        """Add a consumer to the dictionary."""
        with self._lock:
            self._dict[consumer_id] = ThreadSafeCounter()

    def contains(self, consumer_id: str) -> bool:
        """Return whether the dictionary contains the given consumer."""
        with self._lock:
            return consumer_id in self._dict

    def get_offset(self, consumer_id: str) -> int:
        """Return the current offset value."""
        return self._dict[consumer_id].get()

    def get_offset_and_increment(
        self, consumer_id: str, threshold: int
    ) -> int:
        """Get the current offset value and increment it by 1 if it is less
        than the threshold."""
        return self._dict[consumer_id].get_and_increment(threshold)
