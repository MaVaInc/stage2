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
        # Забираем все данные из таблицы AccountState
        account_states = session.query(AccountState).all()
        return account_states
    finally:
        session.close()

# Пример вызова функции
all_accounts = get_all_account_states()

# Печать данных
for account in all_accounts:
    print(account.account_id, account.project_name, account.balances, account.last_executed_task_time)
