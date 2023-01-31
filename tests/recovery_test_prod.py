# make sure to run app with ProdConfig

import requests
from rnn_queue import Consumer, Producer

MESSAGES = 300

response = requests.post(
    "http://localhost:5000/topics", json={"name": "test_topic"}
)

producer = Producer("localhost", 5000)
producer.register("test_topic")

cnt = 0

while True:
    status, message = producer.produce("test_topic", f"test message {cnt}")
    if status:
        cnt += 1
    if cnt == MESSAGES:
        break

print("Prod Done")
producer.close()
