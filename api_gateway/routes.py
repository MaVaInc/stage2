from flask import Blueprint, request, jsonify
from execution_engine.executor import QuestExecutor

routes = Blueprint('routes', __name__)

@routes.route('/process_state', methods=['POST'])
def process_state():
    data = request.json
    account_id = data.get("account_id")
    project_name = data.get("project_name")
    game_state = data.get("game_state")
    task_data = data.get("task_data")

    executor = QuestExecutor(account_id, project_name, task_data)
    action = executor.execute_next_step(game_state)

    return jsonify(action)
