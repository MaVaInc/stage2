from datetime import datetime

from sqlalchemy.testing import db


class AccountState:
    def __init__(self, account_id, project_name, location, step, current_task, last_execution_time):
        self.account_id = account_id
        self.project_name = project_name
        self.location = location
        self.step = step
        self.current_task = current_task
        self.last_execution_time = last_execution_time

    def update_state(self, new_location=None, new_step=None, new_task=None):
        if new_location:
            self.location = new_location
        if new_step is not None:
            self.step = new_step
        if new_task:
            self.current_task = new_task

    def is_task_ready(self, task, timeout):
        current_time = datetime.now()
        return (current_time - self.last_execution_time).total_seconds() > timeout

class Task:
    def __init__(self, name, steps):
        self.name = name
        self.steps = steps

    def get_next_step(self, current_step):
        if current_step < len(self.steps):
            return self.steps[current_step]
        return None
class AccountStateModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String, nullable=False)
    project_name = db.Column(db.String, nullable=False)
    current_location = db.Column(db.String, nullable=True)
    current_task = db.Column(db.String, nullable=True)
    current_step = db.Column(db.Integer, nullable=True)
    last_task_execution = db.Column(db.DateTime, nullable=True)
    task_status = db.Column(db.String, nullable=True)
