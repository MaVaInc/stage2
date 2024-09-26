# account_manager/accounts.py

from db.database import SessionLocal, init_db
from db.models import AccountState
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class AccountManager:
    def __init__(self):
        init_db()
        self.session: Session = SessionLocal()

    def get_account_state(self, account_id, project_name):
        account_state = self.session.query(AccountState).filter_by(
            account_id=account_id,
            project_name=project_name
        ).first()
        if account_state:
            return {
                'balances': account_state.balances,
                'last_executed_task_time': account_state.last_executed_task_time,
                'state_data': account_state.state_data or {}
            }
        else:
            # Создаем новое состояние аккаунта, если не найдено
            new_account_state = AccountState(
                account_id=account_id,
                project_name=project_name,
                balances={},
                last_executed_task_time=None,
                state_data={}
            )
            self.session.add(new_account_state)
            self.session.commit()
            logger.info(f"Создано новое состояние для аккаунта {account_id} проекта {project_name}.")
            return {
                'balances': {},
                'last_executed_task_time': None,
                'state_data': {}
            }

    def update_account_state(self, account_id, project_name, state):
        account_state = self.session.query(AccountState).filter_by(
            account_id=account_id,
            project_name=project_name
        ).first()
        if account_state:
            account_state.balances = state.get('balances', account_state.balances)
            account_state.last_executed_task_time = state.get('last_executed_task_time', account_state.last_executed_task_time)
            account_state.state_data = state.get('state_data', account_state.state_data)
            self.session.commit()
            logger.info(f"Обновлено состояние аккаунта {account_id} проекта {project_name}.")
        else:
            logger.error(f"Аккаунт {account_id} проекта {project_name} не найден.")

    def add_account(self, account_id, project_name, balances=None):
        account_state = self.session.query(AccountState).filter_by(
            account_id=account_id,
            project_name=project_name
        ).first()
        if account_state:
            logger.info(f"Аккаунт {account_id} для проекта {project_name} уже существует.")
            return account_state
        new_account_state = AccountState(
            account_id=account_id,
            project_name=project_name,
            balances=balances or {},
            last_executed_task_time=None,
            state_data={}
        )
        self.session.add(new_account_state)
        self.session.commit()
        logger.info(f"Добавлен новый аккаунт {account_id} для проекта {project_name}.")
        return new_account_state
