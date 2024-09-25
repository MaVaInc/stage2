# tests/test_seed_fsm.py

import unittest
from projects.blum import SeedFSM

class TestSeedFSM(unittest.TestCase):
    def setUp(self):
        self.account_id = 'test_user'
        self.game_state = {
            'elements': [
                {'id': 'reward_status', 'type': 'text', 'text': 'Награды не собраны', 'be': False},
                {'id': 'claim_reward_button', 'type': 'xpath', 'value': "//button[@id='claim_reward']", 'be': True},
                # Добавьте другие элементы по необходимости
            ]
        }
        self.fsm = SeedFSM(self.account_id, self.game_state)

    def test_start_game_transition(self):
        self.fsm.start_game()
        self.assertEqual(self.fsm.state, 'start_screen_can_click_claim')

    def test_rewards_available(self):
        # Установим состояние, чтобы награды были доступны
        self.fsm.state = 'earn'
        data = {
            'worm': {
                'type': "//button[@id='claim_reward']",
                'text': 'Claim',
                'be': True
            }
        }
        actions = self.fsm.process_data(data)
        expected_action = {
            'action': 'click',
            'element': {
                'type': 'xpath',
                'value': "//button[@id='claim_reward']",
                'text': 'Claim'
            },
            'data': {}
        }
        self.assertIn(expected_action, actions)
        self.assertEqual(self.fsm.state, 'check_rewards')  # После верификации

    def test_rewards_already_collected(self):
        # Установим состояние, что награды уже собраны
        self.fsm.rewards_fsm.state = 'rewards_already_collected'
        data = {
            'worm': {
                'type': "//button[@id='claim_reward']",
                'text': 'Claim',
                'be': False
            }
        }
        actions = self.fsm.process_data(data)
        self.assertEqual(actions, [])  # Никаких действий не должно быть
        self.assertEqual(self.fsm.state, 'check_rewards')

    def test_collect_rewards_action(self):
        # Установим состояние, что награды доступны и инициируем сбор
        self.fsm.rewards_fsm.state = 'collect_rewards'
        data = {
            'worm': {
                'type': "//button[@id='claim_reward']",
                'text': 'Claim',
                'be': True
            }
        }
        actions = self.fsm.process_data(data)
        expected_action = {
            'action': 'click',
            'element': {
                'type': 'selector',
                'value': "//button[@id='claim_reward']",
                'text': 'Claim'
            },
            'data': {}
        }
        self.assertIn(expected_action, actions)
        self.assertEqual(self.fsm.rewards_fsm.state, 'verify_rewards')

if __name__ == '__main__':
    unittest.main()
