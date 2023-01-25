import threading
from typing import Dict, List, Optional
import uuid
import time

from src.models import Topic, Log


class MasterQueue:
    """
    Master queue is a collection of all the topics.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._topics: Dict[str, Topic] = {}

    def _contains(self, topic_name: str) -> bool:
        """Return whether the master queue contains the given topic."""
        with self._lock:
            return topic_name in self._topics

    def check_and_add_topic(self, topic_name: str) -> None:
        """Add a topic to the master queue."""
        with self._lock:
            if topic_name in self._topics:
                raise Exception("Topic already exists.")
            self._topics[topic_name] = Topic(topic_name)

    def get_size(self, topic_name: str, consumer_id: str) -> int:
        """Return the number of log messages in the requested topic for
        this consumer."""
        if not self._contains(topic_name):
            raise Exception("Topic does not exist.")
        if not self._topics[topic_name].check_consumer(consumer_id):
            raise Exception("Consumer not registered with topic.")
        total_length = self._topics[topic_name].get_length()
        consumer_offset = self._topics[topic_name].get_consumer_offset(consumer_id)
        return total_length - consumer_offset

    def get_log(self, topic_name: str, consumer_id: str) -> Optional[Log]:
        """Return the log if consumer registered with topic and has a log
        available to pull."""
        if not self._contains(topic_name):
            raise Exception("Topic does not exist.")
        if not self._topics[topic_name].check_consumer(consumer_id):
            raise Exception("Consumer not registered with topic.")
        current_length = self._topics[topic_name].get_length()
        index_to_fetch = self._topics[
            topic_name
        ].get_and_increment_consumer_offset(consumer_id, current_length)
        if index_to_fetch == current_length:
            return None
        return self._topics[topic_name].get_log(index_to_fetch)

    def add_log(self, topic_name: str, producer_id: str, message: str) -> None:
        """Add a log to the topic if producer is registered with topic."""
        if not self._contains(topic_name):
            raise Exception("Topic does not exist.")
        if not self._topics[topic_name].check_producer(producer_id):
            raise Exception("Producer not registered with topic.")
        self._topics[topic_name].add_log(
            Log(producer_id, message, time.time())
        )

    def get_topics(self) -> List[str]:
        """Return the topic names."""
        with self._lock:
            return list(self._topics.keys())

    def add_consumer(self, topic_name: str) -> str:
        """Add a consumer to the topic and return its id."""
        if not self._contains(topic_name):
            raise Exception("Topic does not exist.")
        consumer_id = str(uuid.uuid4().hex)
        self._topics[topic_name].add_consumer(consumer_id)
        return consumer_id

    def add_producer(self, topic_name: str) -> str:
        """Add a producer to the topic and return its id."""
        if not self._contains(topic_name):
            raise Exception("Topic does not exist.")
        producer_id = str(uuid.uuid4().hex)
        self._topics[topic_name].add_producer(producer_id)
        return producer_id
