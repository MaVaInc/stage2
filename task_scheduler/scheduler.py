# task_scheduler/scheduler.py

import time
from account_manager.accounts import AccountManager
from datetime import datetime, timedelta
from config import TASK_SCHEDULER_INTERVAL
from utils.logger import log_info

class TaskScheduler:
    def __init__(self):
        self.account_manager = AccountManager()

    def run(self):
        while True:
            self.schedule_tasks()
            time.sleep(TASK_SCHEDULER_INTERVAL)

    def schedule_tasks(self):
        # Получаем все аккаунты из базы данных
        from db.database import session
        from db.models import AccountState

        accounts = session.query(AccountState).all()
        for account in accounts:
            # Проверяем, нужно ли запланировать новую задачу
            # Например, если текущая задача завершена
            if not account.current_task:
                # Планируем новую задачу
                account.current_task = 'daily_quest'  # Можно выбрать задачу по логике
                account.current_step = 0
                session.commit()
                log_info(f"Scheduled new task for account {account.account_id}")

if __name__ == '__main__':
    scheduler = TaskScheduler()
    scheduler.run()
