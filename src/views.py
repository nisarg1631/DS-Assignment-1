from flask import make_response, request, jsonify
from flask_expects_json import expects_json
from jsonschema import ValidationError

from src import app, master_queue, expects_json


@app.errorhandler(400)
def bad_request(error):
    """Bad request handler for ill formated JSONs"""
    if isinstance(error.description, ValidationError):
        return make_response(
            jsonify(
                {"status": "failure", "message": error.description.message}
            ),
            400,
        )
    # handle other bad request errors
    return error


@app.route(rule="/")
def index():
    return make_response("Welcome to Connectify Distributed Queue API!", 200)


@app.route(rule="/topics", methods=["GET", "POST"])
@expects_json(
    {
        "type": "object",
        "properties": {"name": {"type": "string"}},
        "required": ["name"],
    },
    ignore_for=["GET"],
)
def topics():
    """Return all the topics or add a topic."""

    # If method is POST add a topic
    if request.method == "POST":
        topic_name = request.get_json()["name"]
        try:
            master_queue.check_and_add_topic(topic_name)
            return make_response(
                jsonify(
                    {
                        "status": "success",
                        "message": f"Topic '{topic_name}' created successfully.",
                    }
                ),
                200,
            )
        except Exception as e:
            return make_response(
                jsonify({"status": "failure", "message": str(e)}), 400
            )

    # If method is GET return all the topics
    try:
        topics = master_queue.get_topics()
        return make_response(
            jsonify({"status": "success", "topics": topics}), 200
        )
    except Exception as e:
        return make_response(
            jsonify({"status": "failure", "message": str(e)}), 400
        )


@app.route(rule="/register/consumer", methods=["POST"])
@expects_json(
    {
        "type": "object",
        "properties": {"topic": {"type": "string"}},
        "required": ["topic"],
    }
)
def register_consumer():
    """Register a consumer for a topic."""
    topic_name = request.get_json()["topic"]
    try:
        consumer_id = master_queue.add_consumer(topic_name)
        return make_response(
            jsonify({"status": "success", "consumer_id": consumer_id}),
            200,
        )
    except Exception as e:
        return make_response(
            jsonify({"status": "failure", "message": str(e)}), 400
        )


@app.route(rule="/register/producer", methods=["POST"])
@expects_json(
    {
        "type": "object",
        "properties": {"topic": {"type": "string"}},
        "required": ["topic"],
    }
)
def register_producer():
    """Register a producer for a topic."""
    topic_name = request.get_json()["topic"]
    try:
        producer_id = master_queue.add_producer(topic_name)
        return make_response(
            jsonify({"status": "success", "producer_id": producer_id}),
            200,
        )
    except Exception as e:
        return make_response(
            jsonify({"status": "failure", "message": str(e)}), 400
        )


@app.route(rule="/producer/produce", methods=["POST"])
@expects_json(
    {
        "type": "object",
        "properties": {
            "topic": {"type": "string"},
            "producer_id": {"type": "string"},
            "message": {"type": "string"},
        },
        "required": ["topic", "producer_id", "message"],
    }
)
def produce():
    """Add a log to a topic."""
    topic_name = request.get_json()["topic"]
    producer_id = request.get_json()["producer_id"]
    message = request.get_json()["message"]
    try:
        master_queue.add_log(topic_name, producer_id, message)
        return make_response(
            jsonify({"status": "success"}),
            200,
        )
    except Exception as e:
        return make_response(
            jsonify({"status": "failure", "message": str(e)}), 400
        )


@app.route(rule="/consumer/consume", methods=["GET"])
@expects_json(
    {
        "type": "object",
        "properties": {
            "topic": {"type": "string"},
            "consumer_id": {"type": "string"},
        },
        "required": ["topic", "consumer_id"],
    }
)
def consume():
    """Consume a log from a topic."""
    topic_name = request.get_json()["topic"]
    consumer_id = request.get_json()["consumer_id"]
    try:
        log = master_queue.get_log(topic_name, consumer_id)
        if log is not None:
            return make_response(
                jsonify({"status": "success", "message": log.message}), 200
            )
        return make_response(
            jsonify(
                {"status": "failure", "message": "No logs available to pull."}
            ),
            200,
        )
    except Exception as e:
        return make_response(
            jsonify({"status": "failure", "message": str(e)}), 400
        )


@app.route(rule="/size", methods=["GET"])
@expects_json(
    {
        "type": "object",
        "properties": {
            "topic": {"type": "string"},
            "consumer_id": {"type": "string"},
        },
        "required": ["topic", "consumer_id"],
    }
)
def size():
    """Return the number of log messages in the requested topic for this consumer."""
    topic_name = request.get_json()["topic"]
    consumer_id = request.get_json()["consumer_id"]
    try:
        size = master_queue.get_size(topic_name, consumer_id)
        return make_response(jsonify({"status": "success", "size": size}), 200)
    except Exception as e:
        return make_response(
            jsonify({"status": "failure", "message": str(e)}), 400
        )
