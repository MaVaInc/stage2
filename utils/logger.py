# utils/logger.py

import logging

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Консольный обработчик
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Форматтер
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    if not logger.handlers:
        logger.addHandler(ch)
