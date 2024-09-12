from flask import Flask
from scheduler import schedule_task

app = Flask(__name__)

@app.route('/schedule_task', methods=['POST'])
def create_task():
    task_data = request.json
    schedule_task(task_data)
    return {"status": "Task Scheduled"}

if __name__ == '__main__':
    app.run(port=8001)
