class Log:
    """
    Class representing a log message.
    """

    def __init__(self, producer_id: str, message: str, timestamp: float):
        """Initialize a log message."""
        self.producer_id = producer_id
        self.message = message
        self.timestamp = timestamp
