import threading

from src.datastructures import ThreadSafeLogQueue, ThreadSafeConsumerDict, ThreadSafeProducerSet

class Topic():
    """
    A topic is a collection of log messages that are related to each other.
    """
    def __init__(self, name: str):
        self._name = name
        self._logs = ThreadSafeLogQueue()
        self._producers = ThreadSafeProducerSet()
        self._consumers = ThreadSafeConsumerDict()

    def get_length(self) -> int:
        """Return the length of the topic."""
        return len(self._logs)
    
    def get_log(self, index: int) -> Log:
        """Return the log at the given index."""
        return self._logs[index]
    
    def add_log(self, log: Log) -> None:
        """Add a log to the topic."""
        self._logs.append(log)
