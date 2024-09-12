from flask import Blueprint, request, jsonify
from flask_cors import CORS
from api_gateway.app import app
from message_queue.queue import send_task_to_queue

bp = Blueprint('routes', __name__)
CORS(app)

@app.route('/receive_state', methods=['POST'])
def receive_state():
    data = request.json
    account_id = data['account_id']
    project_name = data['project_name']
    state = data['state']

    # Передаем данные в TaskExecutor для обработки
    action = task_executor.process_task(account_id, project_name, state)

    return jsonify(action)

