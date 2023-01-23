import threading
from typing import List

from src.models import Log

class ThreadSafeLogQueue():
    """
    A thread-safe logs queue.

    Note: It is the users responsibility to ensure that the index being
    accessed is within the bounds of the queue. This class does not
    perform any bounds checking.
    """

    def __init__(self):
        self._queue: List[Log] = []
        self._lock = threading.Lock()
    
    def append(self, log: Log) -> None:
        """Append a log to the queue."""
        index = -1
        with self._lock:
            """Optimisation: Write an empty message with the lock on to
            the queue and then write the actual message with the lock
            off. This is because the lock is a bottleneck and we want
            to reduce the time spent on it."""
            index = len(self._queue)
            self._queue.append(Log('', '', 0.0))
        self._queue[index] = log

    def __len__(self) -> int:
        """Return the length of the queue."""
        with self._lock:
            return len(self._queue)
    
    def __getitem__(self, index: int) -> log:
        """Return the log at the given index."""
        return self._queue[index]
