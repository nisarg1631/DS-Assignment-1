# make sure to run app with ProdConfig

import requests
from rnn_queue import Consumer, Producer

MESSAGES = 300

response = requests.post(
    "http://localhost:5000/topics", json={"name": "test_topic"}
)

consumer = Consumer("localhost", 5000)
consumer.register("test_topic")

cnt = 0

while True:
    status, message = consumer.consume("test_topic")
    if status:
        cnt += 1
    if cnt == MESSAGES:
        break

print("Cons Done")
consumer.close()
