# execution_engine/project_executors/blum_executor.py

from execution_engine.base_executor import BaseExecutor
import json
from datetime import datetime

class ProjectAExecutor(BaseExecutor):
    def __init__(self):
        super().__init__()

    def process_state(self, account_id, project_name, state):
        # Получаем состояние аккаунта
        account_state = self.account_manager.get_account_state(account_id, project_name)
        location = state.get('location')
        elements = state.get('elements')
        balance = state.get('balance')  # Получаем информацию о балансе

        # Обновляем баланс и другие параметры
        account_state['balance'] = balance
        account_state['stats'] = state.get('stats')
        account_state['location'] = location
        self.account_manager.update_account_state(account_id, project_name, account_state)

        # Определяем текущую задачу и шаг
        current_task = account_state.get('current_task')
        current_step = account_state.get('current_step', 0)

        # Загружаем задачи для проекта
        tasks = self.load_tasks(project_name)

        # Если нет текущей задачи, выбираем следующую
        if not current_task:
            current_task = self.select_next_task(account_id, project_name, tasks)
            if not current_task:
                return {'status': 'all_tasks_completed'}
            account_state['current_task'] = current_task
            account_state['current_step'] = 0
            self.account_manager.update_account_state(account_id, project_name, account_state)

        # Если текущая задача - 'collect_reward'
        if current_task == 'collect_reward':
            # Выполняем действие по сбору награды
            action_response = {
                'element': 'Кнопка сбора награды',
                'action': 'click'
            }
            # Обновляем время последнего сбора награды
            account_state['state_data']['last_collect_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Сбрасываем текущую задачу
            account_state['current_task'] = None
            account_state['current_step'] = 0
            self.account_manager.update_account_state(account_id, project_name, account_state)
            return action_response

        # Получаем информацию о текущей задаче
        task_info = tasks.get('tasks', {}).get(current_task)
        if not task_info:
            # Обработка отсутствующей задачи
            account_state['current_task'] = None
            self.account_manager.update_account_state(account_id, project_name, account_state)
            return {'status': 'task_not_found'}

        steps = task_info.get('steps', [])
        if current_step >= len(steps):
            # Задача завершена
            account_state['current_task'] = None
            account_state['current_step'] = 0
            self.account_manager.update_account_state(account_id, project_name, account_state)
            # Выполняем действие после задачи
            post_action = task_info.get('post_action', 'return_home')
            if post_action == 'return_home':
                return self.navigate_home()
            return {'status': 'task_completed'}

        # Получаем информацию о текущем шаге
        step_info = steps[current_step]

        # Проверяем, находимся ли мы в нужном месте
        if location != step_info['location']:
            # Переходим в требуемое место
            navigation_task = self.get_navigation_task(location, step_info['location'], project_name)
            if navigation_task:
                # Инициируем навигацию
                account_state['current_task'] = navigation_task
                account_state['current_step'] = 0
                self.account_manager.update_account_state(account_id, project_name, account_state)
                return self.process_state(account_id, project_name, state)
            else:
                return {'status': 'navigation_task_not_found'}

        # Проверяем наличие триггерного элемента
        trigger_element = self.find_element(elements, step_info['trigger_element'])
        if trigger_element:
            # Выполняем действие
            action_response = {
                'element': step_info['trigger_element']['description'],
                'action': step_info['action']
            }
            # Обновляем шаг и ожидаем подтверждения
            account_state['current_step'] += 1
            self.account_manager.update_account_state(account_id, project_name, account_state)
            return action_response
        else:
            return {'status': 'waiting_for_trigger_element'}

    def load_tasks(self, project_name):
        # Загружаем задачи для проекта
        try:
            with open(f'tasks/{project_name}_tasks.json', 'r') as file:
                tasks = json.load(file)
            return tasks
        except FileNotFoundError:
            return {'tasks': {}}

    def select_next_task(self, account_id, project_name, tasks):
        # Логика выбора следующей задачи
        # Например, выбираем первую незавершенную задачу
        for task_name, task_info in tasks.get('tasks', {}).items():
            # Можно добавить условия на основании состояния аккаунта
            return task_name
        return None

    def get_navigation_task(self, current_location, target_location, project_name):
        # Логика выбора задачи навигации
        task_name = f'navigate_from_{current_location}_to_{target_location}'
        tasks = self.load_tasks(project_name)
        if task_name in tasks.get('navigation_tasks', {}):
            return task_name
        # Если нет конкретной задачи навигации, возвращаем задачу по умолчанию
        return 'default_navigation_task'

    def navigate_home(self):
        # Логика возвращения на главный экран
        return {
            'action': 'navigate',
            'location': 'main_screen'
        }

    def find_element(self, elements, trigger_element):
        # Логика поиска триггерного элемента в списке элементов
        for element in elements:
            if element.get('xpath') == trigger_element.get('xpath'):
                return element
        return None
