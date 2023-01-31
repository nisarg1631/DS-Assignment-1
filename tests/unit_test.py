import requests

# Test create topic

response = requests.post(
    "http://localhost:5000/topics", json={"name": "test_topic"}
)
assert response.status_code == 200
assert response.json()["status"] == "success"
assert (
    response.json()["message"] == f"Topic 'test_topic' created successfully."
)

response = requests.post(
    "http://localhost:5000/topics", json={"name": "test_topic2"}
)
assert response.status_code == 200
assert response.json()["status"] == "success"
assert (
    response.json()["message"] == f"Topic 'test_topic2' created successfully."
)

response = requests.post(
    "http://localhost:5000/topics", json={"name": "test_topic2"}
)
assert response.status_code == 400
assert response.json()["status"] == "failure"
assert response.json()["message"] == "Topic already exists."

# Test get topics
response = requests.get("http://localhost:5000/topics")
assert response.status_code == 200
assert response.json()["status"] == "success"
assert response.json()["topics"] == ["test_topic", "test_topic2"]

# Test register consumer
response = requests.post(
    "http://localhost:5000/consumer/register", json={"topic": "test_topic"}
)
assert response.status_code == 200
assert response.json()["status"] == "success"
consumer_id = response.json()["consumer_id"]

response = requests.post(
    "http://localhost:5000/consumer/register", json={"topic": "test_topic3"}
)
assert response.status_code == 400
assert response.json()["status"] == "failure"
assert response.json()["message"] == "Topic does not exist."

# Test register producer
response = requests.post(
    "http://localhost:5000/producer/register", json={"topic": "test_topic"}
)
assert response.status_code == 200
assert response.json()["status"] == "success"
producer_id = response.json()["producer_id"]

response = requests.post(
    "http://localhost:5000/producer/register", json={"topic": "test_topic3"}
)
assert response.status_code == 400
assert response.json()["status"] == "failure"
assert response.json()["message"] == "Topic does not exist."

# Test produce message
response = requests.post(
    "http://localhost:5000/producer/produce",
    json={
        "topic": "test_topic",
        "producer_id": producer_id,
        "message": "test_message",
    },
)
assert response.status_code == 200
assert response.json()["status"] == "success"

response = requests.post(
    "http://localhost:5000/producer/produce",
    json={
        "topic": "test_topic",
        "producer_id": producer_id,
        "message": "test_message2",
    },
)
assert response.status_code == 200
assert response.json()["status"] == "success"

response = requests.post(
    "http://localhost:5000/producer/produce",
    json={
        "topic": "test_topic3",
        "producer_id": producer_id,
        "message": "test_message",
    },
)
assert response.status_code == 400
assert response.json()["status"] == "failure"
assert response.json()["message"] == "Topic does not exist."

response = requests.post(
    "http://localhost:5000/producer/produce",
    json={
        "topic": "test_topic2",
        "producer_id": producer_id,
        "message": "test_message",
    },
)
assert response.status_code == 400
assert response.json()["status"] == "failure"
assert response.json()["message"] == "Producer not registered with topic."

# Test size and consume
response = requests.get(
    "http://localhost:5000/size",
    json={"topic": "test_topic", "consumer_id": consumer_id},
)
assert response.status_code == 200
assert response.json()["status"] == "success"
assert response.json()["size"] == 2

response = requests.get(
    "http://localhost:5000/size",
    json={"topic": "test_topic3", "consumer_id": consumer_id},
)
assert response.status_code == 400
assert response.json()["status"] == "failure"
assert response.json()["message"] == "Topic does not exist."

response = requests.get(
    "http://localhost:5000/size",
    json={"topic": "test_topic2", "consumer_id": consumer_id},
)
assert response.status_code == 400
assert response.json()["status"] == "failure"
assert response.json()["message"] == "Consumer not registered with topic."

response = requests.get(
    "http://localhost:5000/consumer/consume",
    json={"topic": "test_topic", "consumer_id": consumer_id},
)
assert response.status_code == 200
assert response.json()["status"] == "success"
assert response.json()["message"] == "test_message"

response = requests.get(
    "http://localhost:5000/consumer/consume",
    json={"topic": "test_topic3", "consumer_id": consumer_id},
)
assert response.status_code == 400
assert response.json()["status"] == "failure"
assert response.json()["message"] == "Topic does not exist."

response = requests.get(
    "http://localhost:5000/consumer/consume",
    json={"topic": "test_topic2", "consumer_id": consumer_id},
)
assert response.status_code == 400
assert response.json()["status"] == "failure"
assert response.json()["message"] == "Consumer not registered with topic."

response = requests.get(
    "http://localhost:5000/size",
    json={"topic": "test_topic", "consumer_id": consumer_id},
)
assert response.status_code == 200
assert response.json()["status"] == "success"
assert response.json()["size"] == 1

response = requests.get(
    "http://localhost:5000/consumer/consume",
    json={"topic": "test_topic", "consumer_id": consumer_id},
)
assert response.status_code == 200
assert response.json()["status"] == "success"
assert response.json()["message"] == "test_message2"

response = requests.get(
    "http://localhost:5000/size",
    json={"topic": "test_topic", "consumer_id": consumer_id},
)
assert response.status_code == 200
assert response.json()["status"] == "success"
assert response.json()["size"] == 0
