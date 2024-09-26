# api_gateway/app.py

from flask import Flask
from api_gateway.routes import api_routes
from utils.logger import setup_logger
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
setup_logger()
app.register_blueprint(api_routes, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
