import queue
from execution_engine.executor import QuestExecutor

task_queue = queue.Queue()

def send_task_to_queue(task_data):
    """
    Добавляет задачу в очередь для выполнения.
    """
    task_queue.put(task_data)

def process_task_queue():
    """
    Обрабатывает задачи по очереди.
    """
    quest_executor = QuestExecutor()

    while True:
        if not task_queue.empty():
            task_data = task_queue.get()
            quest_executor.process_task(task_data)
