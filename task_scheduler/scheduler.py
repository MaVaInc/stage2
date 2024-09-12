from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

class TaskScheduler:
    def __init__(self, db, task_executor):
        self.db = db
        self.task_executor = task_executor
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def schedule_task(self, account_id, project_name):
        self.scheduler.add_job(
            func=self.run_task,
            trigger='interval',
            hours=3,  # Интервал запуска задачи
            args=[account_id, project_name]
        )

    def run_task(self, account_id, project_name):
        # Получаем текущее состояние и отправляем задачу на выполнение
        state = self.db.get_account_state(account_id, project_name)
        self.task_executor.process_task(account_id, project_name, state)
