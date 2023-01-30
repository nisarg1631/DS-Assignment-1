# Thread-safe datastructures

Specific details of each function have been given in the docstrings of the functions.

## Counter
Thread-safe counter implementation. Used for maintaining the offset of the consumers.

## Consumer Dictionary
Thread-safe dictionary implementation. Used for maintaining the consumer [counters](#counter) againsts their ids.

## Producer Set
Thread-safe set implementation. Used for maintaining the producer ids.

## Log Queue
Thread-safe queue implementation. Used for maintaining the logs of the queue. We only provide append operation. As a design choice we decided that logs once pushed to the queue will be visible to all the consumers even new ones. Thus there is no need for a pop operation.
