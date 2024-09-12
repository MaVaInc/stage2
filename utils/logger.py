import logging

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_action(action, details):
    logging.info(f"Action: {action}, Details: {details}")
