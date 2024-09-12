from flask import Flask, request
from executor import execute_action

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    task_data = request.json
    execute_action(task_data)
    return {"status": "Executed"}

if __name__ == '__main__':
    app.run(port=8003)
