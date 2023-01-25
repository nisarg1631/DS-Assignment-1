import threading
from typing import List

from src.models import Log


class ThreadSafeLogQueue:
    """
    A thread-safe logs queue.

    Note: It is the users responsibility to ensure that the index being
    accessed is within the bounds of the queue. This class does not
    perform any bounds checking.
    """

    def __init__(self) -> None:
        self._queue: List[Log] = []
        self._lock = threading.Lock()

    def append(self, log: Log) -> None:
        """Append a log to the queue."""
        with self._lock:
            self._queue.append(log)

    def __len__(self) -> int:
        """Return the length of the queue."""
        with self._lock:
            return len(self._queue)

    def __getitem__(self, index: int) -> Log:
        """Return the log at the given index."""
        return self._queue[index]
