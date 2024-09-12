class TaskScheduler:
    def __init__(self):
        self.tasks = {}  # Храним задачи для каждого аккаунта

    def add_task(self, account_id, task_data):
        self.tasks[account_id] = task_data

    def get_task(self, account_id):
        return self.tasks.get(account_id)

    def update_task(self, account_id, current_step):
        task = self.tasks.get(account_id)
        if task:
            task["current_step"] = current_step
            self.tasks[account_id] = task

    def is_task_ready(self, account_id):
        # Логика для проверки, можно ли выполнять задачу (таймауты и время)
        task = self.tasks.get(account_id)
        if task and task.get("next_available_time", 0) < time.time():
            return True
        return False
