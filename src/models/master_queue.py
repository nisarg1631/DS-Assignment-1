import threading
from typing import Dict

from src.models import Topic, Log

class MasterQueue():
    """
    Master queue is a collection of all the topics.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._topics: Dict[str, Topic] = {}

    def contains(self, topic_name: str) -> bool:
        """Return whether the master queue contains the given topic."""
        with self._lock:
            return topic_name in self._topics
    
    def check_and_add(self, topic_name: str) -> bool:
        """Add a topic to the master queue."""
        with self._lock:
            if topic_name in self._topics:
                return False
            self._topics[topic_name] = Topic(topic_name)
            return True
    
    def get_topic_length(self, topic_name: str) -> int:
        """Return the length of the topic."""
        return self._topics[topic_name].get_length()

    def get_log(self, topic_name: str, index: int) -> Log:
        """Return the log at the given index."""
        return self._topics[topic_name].get_log(index)

    def add_log(self, topic_name: str, log: Log) -> None:
        """Add a log to the topic."""
        self._topics[topic_name].add_log(log)
