# account_manager/accounts.py

from db.database import session
from db.models import AccountState

class AccountManager:
    def get_account_state(self, account_id, project_name):
        account_state = session.query(AccountState).filter_by(
            account_id=account_id,
            project_name=project_name
        ).first()
        if account_state:
            return {
                'current_task': account_state.current_task,
                'current_step': account_state.current_step,
                'location': account_state.location,
                'balance': account_state.balance,
                'stats': account_state.stats,
                'state_data': account_state.state_data or {}
            }
        else:
            # Создаем новое состояние аккаунта, если не найдено
            new_account_state = AccountState(
                account_id=account_id,
                project_name=project_name,
                state_data={}
            )
            session.add(new_account_state)
            session.commit()
            return {
                'current_task': None,
                'current_step': 0,
                'location': None,
                'balance': None,
                'stats': None,
                'state_data': {}
            }

    def update_account_state(self, account_id, project_name, state):
        account_state = session.query(AccountState).filter_by(
            account_id=account_id,
            project_name=project_name
        ).first()
        if account_state:
            account_state.current_task = state.get('current_task')
            account_state.current_step = state.get('current_step')
            account_state.location = state.get('location')
            account_state.balance = state.get('balance')
            account_state.stats = state.get('stats')
            account_state.state_data = state.get('state_data')
            session.commit()
