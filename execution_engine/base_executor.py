# execution_engine/base_executor.py

from account_manager.accounts import AccountManager

class BaseExecutor:
    def __init__(self):
        self.account_manager = AccountManager()

    def process_state(self, account_id, project_name, state):
        raise NotImplementedError("Метод process_state должен быть реализован в подклассе.")
