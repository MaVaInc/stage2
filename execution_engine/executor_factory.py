# execution_engine/executor_factory.py

from projects.blum import SeedFSM
# Импортируйте другие FSM для других проектов при необходимости

def get_fsm(project_name, account_id, game_state):
    if project_name == 'blum':
        return SeedFSM(account_id, game_state)
    # Добавьте условия для других проектов
    else:
        raise ValueError(f"Неизвестный проект: {project_name}")
