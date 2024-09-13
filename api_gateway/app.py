# api_gateway/app.py

from flask import Flask

from db.database import Base, engine
from routes import api_routes
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(api_routes)
CORS(app)  # Включаем поддержку CORS для всех роутов
Base.metadata.create_all(engine)
if __name__ == '__main__':
    app.run(debug=True, port=5001)
