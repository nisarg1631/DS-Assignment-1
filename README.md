# DS Assignment 1

## Group members contributions

1. Nisarg Upadhyaya [19CS30031] - 33.33% (design and implementation of the in-memory datastructures, design of the database schema, design of library and implementation of async requests module, concurrency testing)
2. Neha Dalmia [19CS30055] - 33.33% (design and implementation of the queue models, design of the database interactions, producer library implementation, unit testing)
3. Rajat Bachhawat [19CS10073] - 33.33% (design and implementation of the HTTP APIs, implementation of the database models and integration with flask application, consumer library implementation, documentation)
4. GitHub Copilot - 0.01% (pair programmer to give comapny while coding, just kidding :P)

## Setup

## Design

The distributed queue has been implemented as a python application with the `Flask` framework for providing HTTP APIs to interact with the queue. For the persistence layer we use a `PostgreSQL` database. 

### Project Structure
- __src__ - the directory containing the primary application with the in-memory datastructures, models and API support
    - __datastructures__ - implementations for the various thread-safe datastructures used in the queue. For more details, check this [README](src/datastructures/README.md)
    - __models__ - implementations for various concepts of the queue such as `Log`, `Topic`, and `Master_Queue` abstracted using classes. For more details, check this [README](src/models/README.md)
    - __views.py__ - the file containing the HTTP API endpoints for interacting with the queue
    - __json_validator.py__ - the file containing the validator for validating the request JSON body based on the provided schema
- __db_models__ - the directory containing the database models for programmatically interacting with the database using `SQLAlchemy`
- __rnn_queue__ - the directory containing the library, providing an interface for interacting with the queue programmatically

### Database Schema

The database schema is as follows:

#### Table `topic` - contains the names of the topics in the queue
- `name` - the primary key of the table, also the name of the topic

#### Table `log` - contains the logs of the queue
- `id` - the primary key of the table, also the unique identifier of the log along with the `topic_name`
- `topic_name` - the [foreign key](#table-topic---contains-the-names-of-the-topics-in-the-queue) to the `topic` table, the topic to which the log belongs, also the unique identifier of the log along with the `id`
- `producer_id` - the [foreign key](#table-producer---contains-the-details-of-the-producers) to the `producer` table, the id of the producer who produced the log
- `message` - the message of the log
- `timestamp` - the timestamp of the log

#### Table `producer` - contains the details of the producers
- `id` - the primary key of the table, also the unique identifier of the producer
- `topic_name` - the [foreign key](#table-topic---contains-the-names-of-the-topics-in-the-queue) to the `topic` table, the topic to which the producer belongs

#### Table `consumer` - contains the details of the consumers
- `id` - the primary key of the table, also the unique identifier of the consumer
- `topic_name` - the [foreign key](#table-topic---contains-the-names-of-the-topics-in-the-queue) to the `topic` table, the topic to which the consumer belongs
- `offset` - the offset of the consumer 

## Testing

### Unit Testing

### Concurrency Testing

### Recovery Testing

## Difficulties

While it was fairly simple to implement the queue in-memory, it required some thought to abstract the in-memory queue into a database model and how we will be interacting with the database. We also had to think about the various edge cases that could arise while interacting with the queue. As we were doing incremental development we decided to implement the database models over and above the in-memory queue. Changes to database were made only after changes to the in-memory datastructures. This had several advantages:

1. We had to make little to no changes to the in-memory queue implementation.
2. As the consistency of the in-memory queue is maintained by the thread-safety of the datastructures, it was easy to maintain the consistency of the database models as well. Only a few edge cases had to be handled.
3. For the read calls, we could simply use our in-memory queue without querying the database. This would reduce the number of database calls and hence the latency of the read calls.

## Hyperparameters


