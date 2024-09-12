from flask import Flask
from api_gateway.routes import routes

app = Flask(__name__)

# Регистрация маршрутов
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(port=5001)
