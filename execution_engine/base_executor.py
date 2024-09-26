# execution_engine/base_executor.py

from abc import ABC, abstractmethod
from account_manager.accounts import AccountManager

class BaseExecutor(ABC):
    def __init__(self, account_manager: AccountManager):
        self.account_manager = account_manager

    @abstractmethod
    def process_state(self, account_id, project_name, game_state):
        pass
