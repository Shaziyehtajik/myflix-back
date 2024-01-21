
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

if __name__ == "__main__":
    # Run the application in debug mode on all available network interfaces
    app.run(host='0.0.0.0', debug=True)
