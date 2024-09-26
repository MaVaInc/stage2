# api_gateway/routes.py

from flask import Blueprint, request, jsonify
from execution_engine.project_executors.executor_factory import get_executor
from account_manager.accounts import AccountManager
from utils.config import PROJECT_COOLDOWNS
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

api_routes = Blueprint('api_routes', __name__)
account_manager = AccountManager()


@api_routes.route('/check_task', methods=['GET'])
def get_available_task():
    """
    Возвращает доступные проекты для выполнения заданий по заданному account_id.
    """
    account_id = request.args.get('account_id')
    if not account_id:
        return jsonify({'error': 'account_id обязателен.'}), 400

    # Получаем все проекты для данного аккаунта
    session = account_manager.session
    from db.models import AccountState
    account_states = session.query(AccountState).filter_by(account_id=account_id).all()
    available_projects = []

    now = datetime.now()
    for account_state in account_states:
        last_time = account_state.last_executed_task_time
        project = account_state.project_name
        cooldown_hours = PROJECT_COOLDOWNS.get(project.lower(), 24)  # По умолчанию 24 часа

        if last_time:
            time_diff = now - last_time
            if time_diff >= timedelta(hours=cooldown_hours):
                available_projects.append(project)
        else:
            # Если задание никогда не выполнялось, проект доступен
            available_projects.append(project)

    if available_projects:
        return jsonify({'available_projects': available_projects}), 200
    else:
        return jsonify({'message': 'Нет доступных заданий для выполнения.'}), 200

@api_routes.route('/process_state', methods=['POST'])
def process_state():
    """
    Обрабатывает состояние игры и возвращает действие для выполнения.
    Ожидает JSON с 'account_id', 'project_name' и 'game_state'.
    """
    data = request.json
    account_id = data.get("account_id")
    project_name = data.get("project_name")
    game_state = data.get("game_state")

    if not account_id or not project_name or game_state is None:
        return jsonify({'error': 'account_id, project_name и game_state обязательны.'}), 400

    try:
        # Проверяем, существует ли аккаунт, если нет — создаем
        account_state = account_manager.get_account_state(account_id, project_name)
        if not account_state:  # Если аккаунта нет, создаем новый аккаунт
            account_manager.add_account(account_id, project_name, game_state.get('balances', {}))
            logger.info(f"Создан новый аккаунт {account_id} для проекта {project_name}.")

        # Создаем executor для обработки состояния
        executor = get_executor(project_name, account_id, account_manager)
        action = executor.process_state(account_id, project_name, game_state)

        return jsonify(action), 200
    except ValueError as ve:
        logger.error(str(ve))
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        logger.error(str(e))
        return jsonify({'error': 'Ошибка при выполнении.'}), 500

