class TaskExecutor:
    def __init__(self, db):
        self.db = db



    def process_task(self, account_id, project_name, state):
        current_task = state['current_task']
        current_step = state['current_step']
        location = state['location']

        steps = self.get_steps_for_task(current_task)
        next_step = steps[current_step]

        if location != next_step['location']:
            # Отправляем команду на перемещение
            return {
                'action': 'navigate',
                'location': next_step['location']
            }

        # Выполняем действие на текущем шаге
        return {
            'action': next_step['action'],
            'element_xpath': next_step['element_xpath']
        }

    def get_steps_for_task(self, task):
        tasks = {
            'complete_quest': [
                {'location': 'main_screen', 'action': 'click', 'element_xpath': '/path/to/quest_tab'},
                {'location': 'quest_screen', 'action': 'click', 'element_xpath': '/path/to/complete_button'},
                {'location': 'quest_screen', 'action': 'verify', 'element_xpath': '/path/to/verification_element'},
                {'location': 'main_screen', 'action': 'navigate', 'element_xpath': '/path/to/home_button'}
            ],
            # Добавить другие задачи
        }
        return tasks.get(task, [])
    def verify_task_completion(self, task, state):
        if task == 'complete_quest':
            # Проверяем, есть ли элемент, подтверждающий выполнение
            completed_element = state['elements'].get('quest_complete')
            if completed_element and completed_element['exists']:
                return True
        return False

class QuestExecutor:
    def __init__(self, account_id, project_name, task_data):
        self.account_id = account_id
        self.project_name = project_name
        self.task_data = task_data
        self.steps = self.task_data.get("steps", [])  # Микро-шаги выполнения задачи
        self.current_step = task_data.get("current_step", 0)

    def execute_next_step(self, game_state):
        """Выполняем следующий шаг квеста"""
        if self.current_step >= len(self.steps):
            return {"status": "completed"}

        step = self.steps[self.current_step]
        element_info = self.find_element(step, game_state)
        if element_info:
            # Если элемент найден, возвращаем действие для фронта
            return {
                "action": step["action"],
                "element_xpath": element_info["xpath"]
            }
        else:
            # Если элемент не найден, возможно, требуется перейти на другую вкладку
            return {"status": "waiting", "message": "Element not found"}

    def find_element(self, step, game_state):
        """Находим элемент в состоянии игры"""
        for element in game_state["elements"]:
            if element["xpath"] == step["xpath"] and element["value"] == step.get("expected_value", ""):
                return element
        return None
