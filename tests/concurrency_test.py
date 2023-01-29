import requests

MESSAGES = 100

response = requests.post(
    "http://localhost:5000/topics", json={"name": "test_topic"}
)
assert response.status_code == 200
assert response.json()["status"] == "success"

counters = [[0 for _ in range(10)] for _ in range(10)]

def prod(i):
    response = requests.post(
        "http://localhost:5000/producer/register",
        json={"topic": "test_topic"},
    )
    producer_id = response.json()["producer_id"]
    for cnt in range(MESSAGES):
        response = requests.post(
            "http://localhost:5000/producer/produce",
            json={
                "producer_id": producer_id,
                "topic": "test_topic",
                "message": f"{i} {cnt}",
            },
        )
    print(f"Producer {i} done")


def cons(i):
    response = requests.post(
        "http://localhost:5000/consumer/register",
        json={"topic": "test_topic"},
    )
    consumer_id = response.json()["consumer_id"]
    remaining = 10
    while True:
        response = requests.get(
            "http://localhost:5000/consumer/consume",
            json={
                "consumer_id": consumer_id,
                "topic": "test_topic",
            },
        )
        success = response.json()["status"]
        message = response.json()["message"]
        if success == "success":
            prodid, msgid = [int(_) for _ in message.split()]
            assert counters[i][prodid] == msgid
            counters[i][prodid] += 1
            if counters[i][prodid] == MESSAGES:
                remaining -= 1
        if remaining == 0:
            break
    print(f"Consumer {i} done")


import threading

threads = []
for i in range(10):
    threads.append(threading.Thread(target=cons, args=(i,)))
    threads.append(threading.Thread(target=prod, args=(i,)))
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
