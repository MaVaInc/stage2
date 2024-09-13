# api_gateway/routes.py

from flask import Blueprint, request, jsonify
from execution_engine.executor import Executor

api_routes = Blueprint('api_routes', __name__)
executor = Executor()

@api_routes.route('/process_state', methods=['POST'])
def process_state():
    data = request.json
    account_id = data.get('account_id')
    project_name = data.get('project_name')
    state = data.get('state')

    action = executor.process_state(account_id, project_name, state)
    return jsonify(action)
