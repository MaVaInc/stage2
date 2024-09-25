# projects/blum/main_fsm.py

from transitions import Machine
import logging

logger = logging.getLogger(__name__)

class BlumFSM:
    states = [
        'Start',
        'Home_CanClaim',
        'Home_CanStartFarming',
        'Home_Farming',
        'End'
    ]

    def __init__(self, account_id, account_manager):
        self.account_id = account_id
        self.account_manager = account_manager

        # Получаем текущее состояние из базы данных
        account_state = self.account_manager.get_account_state(account_id, 'blum')
        current_state = account_state.get('current_state', 'Start')

        # Инициализируем машину состояний
        self.machine = Machine(model=self, states=BlumFSM.states, initial=current_state)

        # Добавляем переходы
        self.machine.add_transition(trigger='to_daily_reward', source='Start', dest='Home_CanClaim', before='action_click_continue')
        self.machine.add_transition(trigger='to_home_can_claim', source='Home_CanClaim', dest='Home_CanStartFarming', before='action_click_claim')
        self.machine.add_transition(trigger='to_home_can_start_farming', source='Home_CanStartFarming', dest='Home_Farming', before='action_click_start_farming')
        self.machine.add_transition(trigger='end', source='Home_Farming', dest='End')

    # Определение действий при переходах
    def action_click_continue(self):
        logger.info(f"Акаунт {self.account_id}: Выполняется действие 'click_continue'")
        # Здесь можно добавить логику клика на 'Continue'
        # Например, отправить команду через Selenium

    def action_click_claim(self):
        logger.info(f"Акаунт {self.account_id}: Выполняется действие 'click_claim'")
        # Логика клика на 'Claim'

    def action_click_start_farming(self):
        logger.info(f"Акаунт {self.account_id}: Выполняется действие 'click_start_farming'")
        # Логика клика на 'Start Farming'

    # Метод для сохранения текущего состояния
    def save_state(self):
        self.account_manager.update_account_state(
            self.account_id,
            'blum',
            self.state
        )
