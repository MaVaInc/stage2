import requests
import json

# URL сервера (локально или на удаленном сервере)
BASE_URL = "http://localhost:8000/api"

# Пример данных для создания аккаунта
create_account_data = {
    'account_id': 'test_account_2',
    'project_name': 'blum',
    'balances': {'coins': 1000, 'gems': 50}
}

# Пример данных для проверки состояния игры
process_state_data = {
    'account_id': 'test_account_1',
    'project_name': 'blum',
    'game_state': {
        'continueButton': False,
        'refresh': False,
        'claim': False,
        'startFarming': False,
        'farming': True,
        'balances': {'coins': 1000, 'gems': 50}
    }
}

# Функция для отправки POST-запроса для создания аккаунта
def create_account():
    url = f"{BASE_URL}/add_account"
    response = requests.post(url, json=create_account_data)
    print(f"Create Account Response: {response.status_code}")
    print(response.json())

# Функция для проверки доступных заданий
def check_task():
    account_id = "test_account_1"
    url = f"{BASE_URL}/check_task?account_id={account_id}"
    response = requests.get(url)
    print(f"Check Task Response: {response.status_code}")
    print(response.json())

# Функция для обработки состояния игры
def process_state():
    url = f"{BASE_URL}/process_state"
    response = requests.post(url, json=process_state_data)
    print(f"Process State Response: {response.status_code}")
    print(response.json())

if __name__ == "__main__":
    # 1. Создаем аккаунт
    # create_account()

    # 2. Проверяем доступные задания для аккаунта
    check_task()

    # 3. Обрабатываем состояние игры
    process_state()
