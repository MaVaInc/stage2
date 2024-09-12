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


from sqlalchemy import Column, Integer, String, JSON, DateTime
from .database import Base


class AccountState(Base):
    __tablename__ = 'account_state'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String, unique=True, nullable=False)
    project_name = Column(String, nullable=False)
    game_state = Column(JSON)
    task_data = Column(JSON)
    last_updated = Column(DateTime)

