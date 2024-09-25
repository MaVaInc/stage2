# projects/blum/seed_fsm.py

from transitions import Machine
from account_manager.accounts import AccountManager
from projects.blum.sub_fsm_rewards import RewardsFSM
import logging

logger = logging.getLogger(__name__)


class SeedFSM:
    states = [
        'initial',
        'start_screen_can_click_claim',
        'start_screen_can_click_news',
        'start_screen_can_get_worm',
        'start_screen_finish',
        'earn',
        'login_bonus',
        'login_bonus_finish',
        'birds_hungry',
        'birds_can_eat',
        'birds_can_happy',
        'birds_can_hunting',
        'birds_eat_finish',
        'birds_happy_finish',
        'birds_hunting_finish',
        'inventory',
    ]

    def __init__(self, account_id, game_state):
        """
        Инициализация машины состояний для аккаунта проекта 'blum'.

        :param account_id: Идентификатор аккаунта
        :param game_state: Текущее состояние игры, полученное от клиента
        """
        self.account_id = account_id
        self.project_name = 'blum'
        self.game_state = game_state
        self.account_manager = AccountManager()

        # Получаем текущее состояние из базы данных
        account_state = self.account_manager.get_account_state(account_id, self.project_name)
        current_state = account_state.get('current_state', 'initial')

        # Инициализируем машину состояний
        self.machine = Machine(model=self, states=SeedFSM.states, initial=current_state)

        # Добавляем переходы
        self.machine.add_transition(
            trigger='start_game',
            source='initial',
            dest='start_screen_can_click_claim',
            before='action_start_game'
        )
        self.machine.add_transition(
            trigger='click_claim',
            source='start_screen_can_click_claim',
            dest='start_screen_can_click_news',
            before='action_click_claim'
        )
        self.machine.add_transition(
            trigger='click_news',
            source='start_screen_can_click_news',
            dest='start_screen_can_get_worm',
            before='action_click_news'
        )
        self.machine.add_transition(
            trigger='get_worm',
            source='start_screen_can_get_worm',
            dest='start_screen_finish',
            before='action_get_worm'
        )
        self.machine.add_transition(
            trigger='finish_start_screen',
            source='start_screen_finish',
            dest='earn',
            before='action_finish_start_screen'
        )

        # Добавляем переходы для состояния 'earn'
        self.machine.add_transition(
            trigger='collect_login_bonus',
            source='earn',
            dest='login_bonus',
            before='action_collect_login_bonus'
        )
        self.machine.add_transition(
            trigger='finish_login_bonus',
            source='login_bonus',
            dest='login_bonus_finish',
            before='action_finish_login_bonus'
        )
        self.machine.add_transition(
            trigger='go_to_inventory',
            source='login_bonus_finish',
            dest='inventory',
            before='action_go_to_inventory'
        )

        # Пример дополнительных переходов
        self.machine.add_transition(
            trigger='birds_hungry_action',
            source='earn',
            dest='birds_hungry',
            before='action_birds_hungry'
        )
        self.machine.add_transition(
            trigger='birds_can_eat_action',
            source='birds_hungry',
            dest='birds_can_eat',
            before='action_birds_can_eat'
        )
        self.machine.add_transition(
            trigger='birds_can_happy_action',
            source='birds_can_eat',
            dest='birds_can_happy',
            before='action_birds_can_happy'
        )
        self.machine.add_transition(
            trigger='birds_can_hunting_action',
            source='birds_can_happy',
            dest='birds_can_hunting',
            before='action_birds_can_hunting'
        )
        self.machine.add_transition(
            trigger='birds_eat_finish_action',
            source='birds_can_eat',
            dest='birds_eat_finish',
            before='action_birds_eat_finish'
        )
        self.machine.add_transition(
            trigger='birds_happy_finish_action',
            source='birds_can_happy',
            dest='birds_happy_finish',
            before='action_birds_happy_finish'
        )
        self.machine.add_transition(
            trigger='birds_hunting_finish_action',
            source='birds_can_hunting',
            dest='birds_hunting_finish',
            before='action_birds_hunting_finish'
        )
        self.machine.add_transition(
            trigger='go_to_inventory_from_birds',
            source='birds_hunting_finish',
            dest='inventory',
            before='action_go_to_inventory'
        )

        # Добавляем переход к суб-машине наград
        self.machine.add_transition(
            trigger='start_reward_check',
            source='earn',
            dest='earn',  # Оставляем в том же состоянии
            before='action_start_reward_check'
        )

        # Инициализируем суб-машину наград
        self.rewards_fsm = RewardsFSM(account_id, self.account_manager, game_state)

    def process_data(self, data):
        """
        Обрабатывает данные от сервера и инициирует соответствующие триггеры.

        :param data: Словарь с данными от сервера
        :return: Список действий, которые нужно выполнить
        """
        actions = []

        # Пример обработки данных для наград
        if 'worm' in data:
            worm_data = data['worm']
            if worm_data.get('be'):
                # Решаем, что делать с наградой
                if self.rewards_fsm.state == 'check_rewards':
                    self.start_reward_check()
                    actions.extend(self.rewards_fsm.process_data(worm_data))

        # Обработка других элементов
        for key, element in data.items():
            if element.get('be'):
                # Пример: если элемент виден, выполнить действие
                if element['type'] == 'click':
                    action = {
                        'action': 'click',
                        'element': {
                            'type': element['type'],
                            'value': element['value'],
                            'text': element.get('text')
                        },
                        'data': {}
                    }
                    actions.append(action)
                elif element['type'] == 'input':
                    action = {
                        'action': 'input',
                        'element': {
                            'type': element['type'],
                            'value': element['value'],
                            'text': element.get('text')
                        },
                        'data': {
                            'input_text': element.get('input_text', '')
                        }
                    }
                    actions.append(action)
                # Добавьте обработку других типов действий по необходимости

        return actions

    # Методы действий
    def action_start_game(self):
        """
        Действие при начале игры.
        """
        logger.info(f"Акаунт {self.account_id}: Начало игры")
        # Дополнительная логика

    def action_click_claim(self):
        """
        Действие при клике на кнопку 'Claim'.
        """
        logger.info(f"Акаунт {self.account_id}: Клик на кнопку 'Claim'")
        # Дополнительная логика

    def action_click_news(self):
        """
        Действие при клике на кнопку 'News'.
        """
        logger.info(f"Акаунт {self.account_id}: Клик на кнопку 'News'")
        # Дополнительная логика

    def action_get_worm(self):
        """
        Действие при получении червяка.
        """
        logger.info(f"Акаунт {self.account_id}: Получение червяка")
        # Дополнительная логика

    def action_finish_start_screen(self):
        """
        Действие при завершении работы с экраном start_screen.
        """
        logger.info(f"Акаунт {self.account_id}: Завершение работы с экраном start_screen")
        # Дополнительная логика

    def action_collect_login_bonus(self):
        """
        Действие при сборе бонуса за вход.
        """
        logger.info(f"Акаунт {self.account_id}: Сбор бонуса за вход")
        # Дополнительная логика

    def action_finish_login_bonus(self):
        """
        Действие при завершении сбора бонуса за вход.
        """
        logger.info(f"Акаунт {self.account_id}: Завершение сбора бонуса за вход")
        # Дополнительная логика

    def action_go_to_inventory(self):
        """
        Действие при переходе в инвентарь.
        """
        logger.info(f"Акаунт {self.account_id}: Переход в инвентарь")
        # Дополнительная логика

    def action_birds_hungry(self):
        """
        Действие для состояния 'birds_hungry'.
        """
        logger.info(f"Акаунт {self.account_id}: Птицы голодны")
        # Дополнительная логика

    def action_birds_can_eat(self):
        """
        Действие для состояния 'birds_can_eat'.
        """
        logger.info(f"Акаунт {self.account_id}: Птицы могут есть")
        # Дополнительная логика

    def action_birds_can_happy(self):
        """
        Действие для состояния 'birds_can_happy'.
        """
        logger.info(f"Акаунт {self.account_id}: Птицы могут быть счастливыми")
        # Дополнительная логика

    def action_birds_can_hunting(self):
        """
        Действие для состояния 'birds_can_hunting'.
        """
        logger.info(f"Акаунт {self.account_id}: Птицы могут охотиться")
        # Дополнительная логика

    def action_birds_eat_finish(self):
        """
        Действие для состояния 'birds_eat_finish'.
        """
        logger.info(f"Акаунт {self.account_id}: Птицы закончили есть")
        # Дополнительная логика

    def action_birds_happy_finish(self):
        """
        Действие для состояния 'birds_happy_finish'.
        """
        logger.info(f"Акаунт {self.account_id}: Птицы закончили быть счастливыми")
        # Дополнительная логика

    def action_birds_hunting_finish(self):
        """
        Действие для состояния 'birds_hunting_finish'.
        """
        logger.info(f"Акаунт {self.account_id}: Птицы закончили охоту")
        # Дополнительная логика

    def action_start_reward_check(self):
        """
        Инициирует проверку наличия доступных наград.
        """
        logger.info(f"Акаунт {self.account_id}: Проверка наград")
        if self.rewards_fsm.check_if_rewards_available():
            self.rewards_fsm.rewards_available()
        else:
            self.rewards_fsm.rewards_already_collected()

    # Метод для сохранения текущего состояния в базу данных
    def save_state(self):
        """
        Сохраняет текущее состояние автомата и состояние суб-машины наград в базу данных.
        """
        self.account_manager.update_account_state(
            self.account_id,
            self.project_name,
            {
                'current_state': self.state,
                'state_data': self.rewards_fsm.account_manager.get_account_state(
                    self.account_id,
                    self.project_name
                ).get('state_data', {})
            }
        )

    def process_actions(self, data):
        """
        Генерирует список действий на основе данных от сервера.

        :param data: Словарь с данными от сервера
        :return: Список действий для выполнения
        """
        actions = []

        # Обработка наград
        if 'worm' in data:
            worm_data = data['worm']
            if self.rewards_fsm.check_if_rewards_available():
                self.rewards_fsm.rewards_available()
                reward_actions = self.rewards_fsm.process_data(worm_data)
                actions.extend(reward_actions)
            else:
                self.rewards_fsm.rewards_already_collected()

        # Обработка других элементов
        for key, element in data.items():
            if key != 'worm' and element.get('be', False):
                action = {
                    'action': element['action'],
                    'element': {
                        'type': element['type'],
                        'value': element['value'],
                        'text': element.get('text')
                    },
                    'data': element.get('data', {})
                }
                actions.append(action)

        return actions
