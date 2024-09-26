import unittest
from api_gateway.app import app
from account_manager.accounts import AccountManager
from db.database import Base, engine, SessionLocal
from db.models import AccountState


class APITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Создаём тестовую базу данных
        Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        # Удаляем тестовую базу данных после всех тестов
        Base.metadata.drop_all(bind=engine)

    def setUp(self):
        # Инициализация тестового клиента и менеджера аккаунтов
        self.app = app.test_client()
        self.account_manager = AccountManager()
        self.session = SessionLocal()

    def tearDown(self):
        # Закрываем сессию и удаляем данные после каждого теста
        self.session.close()

    def test_add_account(self):
        response = self.app.post('/api/add_account', json={
            'account_id': 'test_account',
            'project_name': 'blum',
            'balances': {'coins': 1000, 'gems': 50}
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Аккаунт test_account для проекта blum добавлен.', response.get_data(as_text=True))

        # Проверяем, что аккаунт добавлен в базу данных
        account = self.session.query(AccountState).filter_by(account_id='test_account', project_name='blum').first()
        self.assertIsNotNone(account)
        self.assertEqual(account.balances, {'coins': 1000, 'gems': 50})

    def test_get_available_task(self):
        # Добавляем аккаунт вручную через менеджер
        self.account_manager.add_account('test_account', 'blum')

        response = self.app.get('/api/get_available_task?account_id=test_account')
        self.assertEqual(response.status_code, 200)
        self.assertIn('available_projects', response.get_json())

    def test_process_state(self):
        # Добавляем аккаунт вручную через менеджер
        self.account_manager.add_account('test_account', 'blum')

        response = self.app.post('/api/process_state', json={
            'account_id': 'test_account',
            'project_name': 'blum',
            'game_state': {
                'continueButton': True,
                'refresh': False,
                'claim': False,
                'startFarming': False,
                'farming': False,
                'balances': {'coins': 1000, 'gems': 50}
            }
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['action'], 'click')


if __name__ == '__main__':
    unittest.main()
