from flask import Flask

# Initialize the app directly
app = Flask(__name__)

# Import routes to register them
from . import routes