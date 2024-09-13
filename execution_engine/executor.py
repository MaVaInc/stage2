# execution_engine/executor.py
from account_manager.accounts import AccountManager


class Executor:
    def __init__(self):
        self.account_manager = AccountManager()

    def process_state(self, account_id, project_name, state):
        account_state = self.account_manager.get_account_state(account_id, project_name)
        location = state.get('location')
        elements = state.get('elements')
        balance = state.get('balance')  # New: Capture balance info

        # Update balance
        if balance:
            account_state['balance'] = balance
            self.account_manager.update_account_state(account_id, project_name, account_state)

        # Determine current task and step
        current_task = account_state.get('current_task')
        current_step = account_state.get('current_step', 0)

        tasks = self.load_tasks(project_name)

        # If no current task, select the next one
        if not current_task:
            current_task = self.select_next_task(account_id, project_name)
            if not current_task:
                return {'status': 'all_tasks_completed'}
            account_state['current_task'] = current_task
            account_state['current_step'] = 0
            self.account_manager.update_account_state(account_id, project_name, account_state)

        # Fetch the current task's steps
        task_info = tasks.get('tasks', {}).get(current_task)
        if not task_info:
            # Handle missing task definition
            account_state['current_task'] = None
            self.account_manager.update_account_state(account_id, project_name, account_state)
            return {'status': 'task_not_found'}

        steps = task_info.get('steps', [])
        if current_step >= len(steps):
            # Task completed
            account_state['current_task'] = None
            account_state['current_step'] = 0
            self.account_manager.update_account_state(account_id, project_name, account_state)
            # Perform post-task action
            post_action = task_info.get('post_action', 'return_home')
            if post_action == 'return_home':
                return self.navigate_home()
            return {'status': 'task_completed'}

        # Get current step details
        step_info = steps[current_step]

        # Check if we are in the correct location
        if location != step_info['location']:
            # Navigate to the required location
            navigation_task = self.get_navigation_task(location, step_info['location'])
            if navigation_task:
                # Initiate navigation
                account_state['current_task'] = navigation_task
                account_state['current_step'] = 0
                self.account_manager.update_account_state(account_id, project_name, account_state)
                return self.process_state(account_id, project_name, state)
            else:
                return {'status': 'navigation_task_not_found'}

        # Check for trigger element
        trigger_element = self.find_element(elements, step_info['trigger_element'])
        if trigger_element:
            # Perform the action
            action_response = {
                'action': step_info['action'],
                'element_xpath': step_info['trigger_element']['xpath']
            }
            # Update step and possibly wait for confirmation
            account_state['current_step'] += 1
            self.account_manager.update_account_state(account_id, project_name, account_state)
            return action_response
        else:
            return {'status': 'waiting_for_trigger_element'}

    def get_navigation_task(self, current_location, target_location):
        # Logic to select the appropriate navigation task
        # For simplicity, assume navigation tasks are named 'navigate_from_{current}_to_{target}'
        task_name = f'navigate_from_{current_location}_to_{target_location}'
        tasks = self.load_tasks()
        if task_name in tasks.get('navigation_tasks', {}):
            return task_name
        # If no specific navigation task, return a default one
        return 'default_navigation_task'

    def navigate_home(self):
        # Logic to navigate back to the home screen
        return {
            'action': 'navigate',
            'location': 'main_screen'
        }

    # Rest of the methods remain the same
