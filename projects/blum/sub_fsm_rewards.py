# projects/blum/rewards_fsm.py

from transitions import Machine
import logging

logger = logging.getLogger(__name__)


class RewardsFSM:
    states = [
        'check_rewards',
        'collect_rewards',
        'verify_rewards',
        'rewards_already_collected'
    ]

    def __init__(self, account_id, account_manager, game_state):
        self.account_id = account_id
        self.account_manager = account_manager
        self.game_state = game_state

        # Инициализируем машину состояний для наград
        self.machine = Machine(model=self, states=RewardsFSM.states, initial='check_rewards')

        # Определяем переходы
        self.machine.add_transition(
            trigger='rewards_available',
            source='check_rewards',
            dest='collect_rewards',
            before='action_rewards_available'
        )
        self.machine.add_transition(
            trigger='rewards_already_collected',
            source='check_rewards',
            dest='rewards_already_collected',
            before='action_rewards_already_collected'
        )
        self.machine.add_transition(
            trigger='collect_rewards_action',
            source='collect_rewards',
            dest='verify_rewards',
            before='action_collect_rewards'
        )
        self.machine.add_transition(
            trigger='verify_rewards_action',
            source='verify_rewards',
            dest='check_rewards',
            before='action_verify_rewards'
        )

    # Методы действий
    def action_rewards_available(self):
        logger.info(f"Акаунт {self.account_id}: Награды доступны для сбора")
        # Логика перехода к сбору наград
        self.collect_rewards_action()

    def action_rewards_already_collected(self):
        logger.info(f"Акаунт {self.account_id}: Награды уже были собраны сегодня")
        # Логика обработки уже собранных наград

    def action_collect_rewards(self):
        logger.info(f"Акаунт {self.account_id}: Сбор наград")
        # Логика сбора наград
        self.verify_rewards_action()

    def action_verify_rewards(self):
        logger.info(f"Акаунт {self.account_id}: Проверка сбора наград")
        if self.verify_rewards_collected():
            logger.info(f"Акаунт {self.account_id}: Награды успешно собраны")
            self.set_rewards_collected_flag()
        else:
            logger.warning(f"Акаунт {self.account_id}: Награды не были собраны")

    def verify_rewards_collected(self):
        """
        Проверяет, были ли награды успешно собраны.
        """
        elements = self.game_state.get('elements', [])
        for el in elements:
            if el['id'] == 'reward_status' and el.get('text') == 'Награды собраны':
                return True
        return False

    def set_rewards_collected_flag(self):
        """
        Устанавливает флаг в базе данных, что награды собраны.
        """
        state_data = self.account_manager.get_account_state(self.account_id, 'blum').get('state_data', {})
        state_data['rewards_collected'] = True
        self.account_manager.update_account_state(
            self.account_id,
            'blum',
            {
                'state_data': state_data
            }
        )

    def process_data(self, worm_data):
        """
        Обрабатывает данные для наград и инициирует соответствующие действия.

        :param worm_data: Данные для награды
        :return: Список действий
        """
        actions = []

        if self.state == 'check_rewards':
            if worm_data.get('be'):
                self.rewards_available()
            else:
                self.rewards_already_collected()

        elif self.state == 'collect_rewards':
            # Здесь предполагается, что после collect_rewards_action()
            # уже выполнено действие и переход в verify_rewards
            actions.append({
                'action': 'click',
                'element': {
                    'type': 'selector',  # Пример
                    'value': worm_data['type'],  # Селектор из данных
                    'text': worm_data.get('text')
                },
                'data': {}
            })

        elif self.state == 'verify_rewards':
            if self.verify_rewards_collected():
                self.set_rewards_collected_flag()
            else:
                # Возможно, повторная попытка или логирование ошибки
                pass

        return actions
