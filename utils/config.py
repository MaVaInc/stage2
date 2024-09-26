# utils/config.py

import os

# Строка подключения к базе данных
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, '..', 'task_scheduler', 'accounts.db')
DATABASE_URI = 'postgresql://myuser:Mavaincee2020@localhost:5433/telegadb'
SQLALCHEMY_DATABASE_URI = 'postgresql://myuser:Mavaincee2020@localhost:5433/telegadb'

# Кулдауны для каждого проекта (в часах)
PROJECT_COOLDOWNS = {
    'blum': 24,
    'projectA': 12,
    'projectB': 48
    # Добавьте другие проекты по мере необходимости
}

# Интервал проверки планировщика задач (в секундах)
TASK_SCHEDULER_INTERVAL = 60  # Например, 60 секунд
