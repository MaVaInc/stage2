# db/models.py

from sqlalchemy import Column, Integer, String, JSON, DateTime, UniqueConstraint
from db.database import Base

class AccountState(Base):
    __tablename__ = 'account_states'
    __table_args__ = (UniqueConstraint('account_id', 'project_name', name='_account_project_uc'),)

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, nullable=False)
    project_name = Column(String, nullable=False)
    balances = Column(JSON, nullable=True)
    last_executed_task_time = Column(DateTime, nullable=True)
    state_data = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<AccountState(account_id='{self.account_id}', project_name='{self.project_name}')>"
