import os.path
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import AccountState  # Импортируй свою модель
from utils.config import DATABASE_URI  # Путь к базе данных

# Настраиваем подключение к базе данных
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для извлечения данных из таблицы AccountState
def get_all_account_states():
    session = SessionLocal()
    try:
        account_states = session.query(AccountState).all()
        return account_states
    finally:
        session.close()

# Пример вызова функции
all_accounts = get_all_account_states()

# Подготовка данных для отправки
def prepare_data_for_google_sheets(data):
    # Уникальные аккаунты и проекты
    unique_accounts = list(set(account.account_id for account in data))
    unique_projects = list(set(account.project_name for account in data))

    # Стартовая строка — проекты по горизонтали
    values = [['Account ID'] + unique_projects]

    # Создание пустой таблицы для заполнения
    for account_id in unique_accounts:
        row = [account_id]
        for project in unique_projects:
            # Поиск аккаунта с проектом
            account_balance = next(
                (account.balances for account in data if account.account_id == account_id and account.project_name == project),
                {}
            )
            # Добавляем баланс в таблицу
            row.append(json.dumps(account_balance) if account_balance else '{}')
        values.append(row)

    # Добавляем строку с суммами по каждому проекту
    totals_row = ['Total']
    for project in unique_projects:
        total_balance = 0
        for account in data:
            if account.project_name == project and 'coins' in account.balances:
                total_balance += account.balances['coins']
        totals_row.append(total_balance)
    values.append(totals_row)

    return values

# ID Google Sheet и диапазон, куда ты будешь отправлять данные
SPREADSHEET_ID = '1X8i1qg1pOT2eNQX-qe70GTtjaZpiXTcRbMJwAx1-pGA'
RANGE_NAME = 'testBalanceSheet!A1'

# Настройка авторизации через service account
SERVICE_ACCOUNT_FILE = '/home/roman/project/pycharm_projects/stage2/utils/temshchiki-1dd2cea4fb48.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)

# Функция для отправки данных в Google Sheets
def send_data_to_google_sheets(data):
    try:
        values = prepare_data_for_google_sheets(data)

        body = {'values': values}

        # Отправляем данные в Google Sheets
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()
        print(f"{result.get('updatedCells')} ячеек обновлено.")
    except HttpError as error:
        print(f"Произошла ошибка: {error}")

# Пример вызова функции
send_data_to_google_sheets(all_accounts)
