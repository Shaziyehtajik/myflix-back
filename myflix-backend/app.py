import logging
from flask import Flask
from flask_cors import CORS
from myflix-backend.api import api_page

app = Flask(__name__)

# Load configuration from the specified file
app.config.from_pyfile('settings.py')

# Enable CORS for all routes
CORS(app)

# Register the API blueprint
app.register_blueprint(api_page)

# Enable debugging mode
app.debug = True

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set the log level to DEBUG

if __name__ == "__main__":
    # Run the application on all available network interfaces
    app.run(host='0.0.0.0')
