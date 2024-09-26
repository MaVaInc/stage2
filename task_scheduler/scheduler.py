# task_scheduler/scheduler.py

import time
from account_manager.accounts import AccountManager
from datetime import datetime, timedelta
from utils.config import PROJECT_COOLDOWNS, TASK_SCHEDULER_INTERVAL
from utils.logger import setup_logger
import logging

setup_logger()
logger = logging.getLogger(__name__)

class TaskScheduler:
    def __init__(self):
        self.account_manager = AccountManager()
        self.cooldowns = PROJECT_COOLDOWNS

    def run(self):
        """
        Запускает бесконечный цикл для проверки доступных заданий.
        """
        while True:
            self.schedule_tasks()
            time.sleep(TASK_SCHEDULER_INTERVAL)  # Проверять каждые TASK_SCHEDULER_INTERVAL секунд

    def schedule_tasks(self):
        """
        Проверяет все аккаунты и планирует доступные задания.
        """
        session = self.account_manager.session
        from db.models import AccountState

        accounts = session.query(AccountState).all()
        now = datetime.now()

        for account in accounts:
            last_time = account.last_executed_task_time
            project = account.project_name
            cooldown_hours = self.cooldowns.get(project.lower(), 24)  # По умолчанию 24 часа

            if last_time:
                time_diff = now - last_time
                if time_diff >= timedelta(hours=cooldown_hours):
                    # Планируем выполнение задания
                    logger.info(f"Планируется выполнение задания для аккаунта {account.account_id} проекта {project}.")
                    # Здесь можно добавить логику отправки задания или его выполнения
            else:
                # Если задание никогда не выполнялось, планируем его
                logger.info(f"Планируется первое выполнение задания для аккаунта {account.account_id} проекта {project}.")
                # Здесь можно добавить логику отправки задания или его выполнения

if __name__ == '__main__':
    scheduler = TaskScheduler()
    scheduler.run()
