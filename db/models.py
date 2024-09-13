# db/models.py

from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class AccountState(Base):
    __tablename__ = 'account_states'

    id = Column(Integer)
    account_id = Column(String, primary_key=True)
    project_name = Column(String)
    current_task = Column(String)
    current_step = Column(Integer)
    location = Column(String)
    balance = Column(JSON)  # Новое поле для хранения баланса в формате JSON
    stats = Column(JSON)    # Новое поле для дополнительной статистики
