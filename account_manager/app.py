from flask import Flask, jsonify
from accounts import get_account_status

app = Flask(__name__)

@app.route('/account/<account_id>', methods=['GET'])
def account_status(account_id):
    return jsonify(get_account_status(account_id))

if __name__ == '__main__':
    app.run(port=8002)
