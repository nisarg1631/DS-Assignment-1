# DS Assignment 1

## Group members contributions

1. Nisarg Upadhyaya [19CS30031] - 33.33% (design and implementation of the in-memory datastructures, design of the database schema, design of library and implementation of async requests module, concurrency testing)
2. Neha Dalmia [19CS30055] - 33.33% (design and implementation of the queue models, design of the database interactions, producer library implementation, unit testing)
3. Rajat Bachhawat [19CS10073] - 33.33% (design and implementation of the HTTP APIs, implementation of the database models and integration with flask application, consumer library implementation, documentation)
4. GitHub Copilot - 0.01% (pair programmer to give comapny while coding, just kidding :P)

## Setup

1. Under a (preferably new) python3 virtual environment, run `pip install -r requirements.txt` to install the dependencies.

2. Configure the `PostgreSQL` database connection by setting the `SQLALCHEMY_DATABASE_URI` in the `config.py` file. Both read and write access is required.

3. Run `python app.py` to start the application.

## Design

The distributed queue has been implemented as a python application with the `Flask` framework for providing HTTP APIs to interact with the queue. For the persistence layer we use a `PostgreSQL` database. An execution of a request is as follows:

1. The HTTP API endpoint is called with the appropriate parameters.
2. The request is validated for schema using a decorator made in the `json_validator.py` file.
3. The request is processed by the `views.py` file.
4. The function in the `views.py` file extracts the parameters from the request and calls the appropriate function on the `master_queue` object initialized at the start of the application.
5. The `master_queue` object does the necessary checks and database interactions and returns the appropriate response or throws an exception.
6. The function in the `views.py` file returns the appropriate response to the HTTP API endpoint based on the response from the `master_queue` object.

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
Test all the individual API endpoints using the `requests` library. Checked both the positive and negative cases.

### Concurrency Testing
Test the thread-safety of the in-memory datastructures using the `threading` library. Created 10 producer threads and 10 consumer threads which would be interacting with the queue simultaneously. Checked that the consumer threads are able to consume the logs in the order they were produced by the producer threads. Ensured ordering by logging messages of the format `<producer_id> <log_id>`. While consuming the `<log_id>` should be in increasing order for each `<producer_id>`. The number of messages to be produced can be set by the `MESSAGES` parameter in the test file.

### Recovery Testing
Test the recovery of the queue from a crash. Start a producer and a consumer. Kill the application. Start the application again. Check that the producer and consumer are able to interact with the queue as before. The producer should be able to produce logs and the consumer should be able to consume logs as long as the limit is not reached. Limit can be set by the `MESSAGES` parameter in the respective test files.

### Performance Testing
We tested both the performance of the queue and the library we provide. We used `asyncio` to make asynchronous requests to the queue using the library. With async consume calls we saw a 50% reduction in time taken to consume the logs. Also we saw a 30-40% improvement in the time taken to process multiple requests with threading enabled in the flask application.

## Difficulties

While it was fairly simple to implement the queue in-memory, it required some thought to abstract the in-memory queue into a database model and how we will be interacting with the database. We also had to think about the various edge cases that could arise while interacting with the queue. As we were doing incremental development we decided to implement the database models over and above the in-memory queue. Changes to database were made only after changes to the in-memory datastructures. This had several advantages:

1. We had to make little to no changes to the in-memory queue implementation.
2. As the consistency of the in-memory queue is maintained by the thread-safety of the datastructures, it was easy to maintain the consistency of the database models as well. Only a few edge cases had to be handled.
3. For the read calls, we could simply use our in-memory queue without querying the database. This would reduce the number of database calls and hence the latency of the read calls.

## Hyperparameters

There are no hyperparameters in the queue itself. However in the library implementation as we have used the async requests module, we have provided the user with the option to set the number of requests to be made in parallel. This can be set by the `parallel_requests` parameter in the `async_requests` class. There are also other parameters such as `limit_per_host` and `limit` which can be used to limit the number of requests to be made to a particular host and the total number of requests to be made respectively. These parameters are provided by the `aiohttp` library. The `ttl_dns_cache` parameter can be used to set the time-to-live of the DNS cache. This parameter is also provided by the `aiohttp` library.
