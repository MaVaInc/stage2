# execution_engine/project_executors/blum_executor.py

import logging
from datetime import datetime, timedelta
from execution_engine.base_executor import BaseExecutor
from utils.config import PROJECT_COOLDOWNS

logger = logging.getLogger(__name__)


class BlumExecutor(BaseExecutor):
    def process_state(self, account_id, project_name, game_state):
        """
        Обрабатывает состояние игры и возвращает соответствующее действие.
        Обновляет базу данных с деталями действия.

        :param account_id: Идентификатор аккаунта
        :param project_name: Название проекта
        :param game_state: Состояние игры, полученное от браузера
        :return: Словарь с действием, элементом и датой
        """
        action_response = {'action': 'noop', 'element': {}, 'date': None}

        # Получаем конфиг кулдауна для проекта
        cooldown_hours = PROJECT_COOLDOWNS.get(project_name.lower(), 24)  # По умолчанию 24 часа

        # Получаем текущее состояние аккаунта
        account_state = self.account_manager.get_account_state(account_id, project_name)
        last_executed_time = account_state.get('last_executed_task_time')
        now = datetime.now()

        # Проверяем кулдаун
        if last_executed_time:
            time_diff = now - last_executed_time
            if time_diff < timedelta(hours=cooldown_hours):
                logger.info(f"Аккаунт {account_id} проекта {project_name}: Кулдаун ещё не истёк.")
                return action_response  # Кулдаун не истёк, никаких действий

        if game_state.get('continueButton'):
            action_response = {
                'action': 'click',
                'element': {
                    'name': 'continueButton',
                    'text': 'Continue',
                },
                'date': now.strftime('%Y-%m-%d %H:%M:%S')
            }


            logger.info(f"Аккаунт {account_id}: Выполнено действие 'click_continue'.")

        elif game_state.get('refresh'):
            action_response = {
                'action': 'refresh',
                'element': {
                    'name': 'refresh',
                    'text': 'Refresh',
                },
                'date': now.strftime('%Y-%m-%d %H:%M:%S')
            }

            logger.info(f"Аккаунт {account_id}: Выполнено действие 'refresh'.")

        elif game_state.get('claim'):
            action_response = {
                'action': 'click',
                'element': {
                    'name': 'claim',
                    'text': 'Claim',
                },
                'date': now.strftime('%Y-%m-%d %H:%M:%S')
            }

            logger.info(f"Аккаунт {account_id}: Выполнено действие 'click_claim'.")

        elif game_state.get('startFarming'):
            action_response = {
                'action': 'click',
                'element': {
                    'name': 'startFarming',
                    'text': 'Start Farming',
                },
                'date': now.strftime('%Y-%m-%d %H:%M:%S')
            }

            logger.info(f"Аккаунт {account_id}: Выполнено действие 'click_start_farming'.")

        elif game_state.get('farming'):
            # Сохраняем действие 'exit' в базе данных
            exit_time = now.strftime('%Y-%m-%d %H:%M:%S')
            action_response = {
                'action': 'exit',
                'element': {
                    'name': 'None',
                    'text': 'None'
                },
                'date': exit_time
            }
            self.account_manager.update_account_state(
                account_id,
                project_name,
                {
                    'balances': game_state.get('balances'),
                    'last_executed_task_time': now,
                    'state_data': {
                        'last_action': 'exit',
                        'last_action_time': exit_time,
                        'exit_task': 'farming'
                    }
                }
            )
            logger.info(f"Аккаунт {account_id}: Выполнено действие 'exit'.")

        else:
            logger.info(f"Аккаунт {account_id}: Нет действий для выполнения.")

        return action_response
