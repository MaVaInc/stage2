# db/models.py

from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class AccountState(Base):
    __tablename__ = 'account_states'

    id = Column(Integer, primary_key=True)
    account_id = Column(String, unique=True, nullable=False)
    project_name = Column(String, nullable=False)
    current_task = Column(String)
    current_step = Column(Integer, default=0)
    location = Column(String)
    balance = Column(JSON)  # Хранит баланс в формате JSON
    stats = Column(JSON)    # Дополнительные статистические данные
    state_data = Column(JSON)  # Хранит дополнительные данные состояния
    current_state = Column(String, default='initial')  # Текущее состояние FSM
