# execution_engine/project_executors/executor_factory.py

from execution_engine.project_executors.blum_executor import BlumExecutor
# Здесь можно добавить другие экзекьюторы для других проектов

def get_executor(project_name, account_id, account_manager):
    if project_name.lower() == 'blum':
        return BlumExecutor(account_manager)
    # Добавьте условия для других проектов
    else:
        raise ValueError(f"Неизвестный проект: {project_name}")
