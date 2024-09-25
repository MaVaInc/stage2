# task_scheduler/scheduler.py

import time
from account_manager.accounts import AccountManager
from datetime import datetime, timedelta
from add_user import TASK_SCHEDULER_INTERVAL
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
            if not account.current_task:
                # Проверяем, пора ли напомнить пользователю о награде
                if self.check_reward_time(account):
                    account.current_task = 'collect_reward'
                    account.current_step = 0
                    session.commit()
                    log_info(f"Scheduled 'collect_reward' task for account {account.account_id}")

    def check_reward_time(self, account):
        # Логика проверки, пора ли напомнить пользователю забрать награду
        # Например, если прошло 24 часа с последнего сбора награды
        last_collect_time = account.state_data.get('last_collect_time')
        if not last_collect_time:
            return True  # Никогда не собирал награду
        last_collect_datetime = datetime.strptime(last_collect_time, '%Y-%m-%d %H:%M:%S')
        if datetime.now() - last_collect_datetime >= timedelta(hours=24):
            return True
        return False

if __name__ == '__main__':
    scheduler = TaskScheduler()
    scheduler.run()
