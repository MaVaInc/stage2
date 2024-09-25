import requests
import urllib.parse
import json


def extract_user_id(init_params):
    parsed_params = urllib.parse.parse_qs(init_params)
    user_param = parsed_params.get('user')
    if not user_param:
        print("Параметр 'user' не найден.")
        return None
    user_json = urllib.parse.unquote(user_param[0])
    try:
        user_data = json.loads(user_json)
        return user_data.get('id')
    except json.JSONDecodeError:
        print("Ошибка при декодировании JSON.")
        return None


def add_user(server_url, user_id):
    url = f"{server_url}/wkblanw"
    payload = {"userId": user_id}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            print("Пользователь успешно добавлен:", response.json())
        else:
            print(f"Ошибка при добавлении пользователя: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def main():
    server_url = "https://proclick.click"  # Замените на ваш URL сервера при необходимости

    # Ваша строка с параметрами (пример)
    # init_params = "query_id=AAEL7ZwuAwAAAAvtnC7QLBL9&user=%7B%22id%22%3A7224487179%2C%22first_name%22%3A%22Andrew%22%2C%22last_name%22%3A%22Thompson%F0%9F%A6%B4%22%2C%22username%22%3A%22fdishfis%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1727096949&hash=496106450a677c66c21c7c8b9c769bcff1641256f29d6dec13e093736f47be26"
    #
    # user_id = extract_user_id(init_params)
    user_id = '6665668482'
    if user_id:
        add_user(server_url, user_id)
    else:
        print("Не удалось извлечь userId.")


if __name__ == "__main__":
    main()
