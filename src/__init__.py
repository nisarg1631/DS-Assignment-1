from flask import Flask
from src.models import MasterQueue
from src.json_validator import expects_json

app = Flask(__name__)
master_queue = MasterQueue()

from src import views
