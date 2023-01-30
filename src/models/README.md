# Models

Specific details of each function have been given in the docstrings of the functions.

## Log
Class for storing the log data. It has the following attributes:
1. producer_id: Id of the producer
2. message: Message to be logged
3. timestamp: Timestamp of the log

## Topic
Class for grouping the logs. It has the following attributes:
1. name: Name of the topic
2. logs: List of logs in the topic (Implemented using [Log Queue](../datastructures/README.md#log-queue)
3. consumers: Dictionary of consumers registered with the topic (Implemented using [Consumer Dictionary](../datastructures/README.md#consumer-dictionary)
4. producers: Set of producers registered with the topic (Implemented using [Producer Set](../datastructures/README.md#producer-set)

## Master Queue
Class for maintaining the topics. It serves as the interface between the flask app and the datastructures. It has a single dictionary attribute `topics` which maps the topic name to the [topic](#topic) object. A single global instance of this class is created when the flask app is started. All requests hitting the flask app are forwarded to this instance to perform the required operations.
