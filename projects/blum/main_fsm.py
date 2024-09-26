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

    def __init__(self, account_id, account_manager, game_state):
        self.account_id = account_id
        self.account_manager = account_manager
        self.game_state = game_state

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
        logger.info(f"Account {self.account_id}: Executing action 'click_continue'")
        # Здесь можно добавить логику действия, если необходимо

    def action_click_claim(self):
        logger.info(f"Account {self.account_id}: Executing action 'click_claim'")
        # Здесь можно добавить логику действия, если необходимо

    def action_click_start_farming(self):
        logger.info(f"Account {self.account_id}: Executing action 'click_start_farming'")
        # Здесь можно добавить логику действия, если необходимо

    # Метод для сохранения текущего состояния
    def save_state(self):
        self.account_manager.update_account_state(
            self.account_id,
            'blum',
            {
                'current_task': self.state,
                'current_step': 0,  # Сбрасываем шаг после перехода
                'location': None,    # Обновите при необходимости
                'balance': None,     # Обновите при необходимости
                'stats': None,       # Обновите при необходимости
                'state_data': {},    # Обновите при необходимости
                'current_state': self.state
            }
        )
