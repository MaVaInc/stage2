# api_gateway/routes.py

from flask import Blueprint, request, jsonify
from execution_engine.executor_factory import get_executor

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/process_state', methods=['POST'])
def process_state():
    data = request.json
    account_id = data.get("account_id")
    project_name = data.get("project_name")
    game_state = data.get("game_state")

    # Получаем соответствующий Executor для проекта
    executor = get_executor(project_name)
    action = executor.process_state(account_id, project_name, game_state)

    return jsonify(action)
