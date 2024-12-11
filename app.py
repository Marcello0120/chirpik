from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock database for simplicity (use a real database for production)
users = {}

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    if username in users:
        return jsonify({'error': 'Account already exists'}), 400
    
    users[username] = {'balance': 0}
    return jsonify({'message': f'Account created for {username}'}), 201

@app.route('/check_balance', methods=['GET'])
def check_balance():
    username = request.args.get('username')
    
    if username not in users:
        return jsonify({'error': 'Account does not exist'}), 404
    
    balance = users[username]['balance']
    return jsonify({'username': username, 'balance': balance}), 200

@app.route('/make_transaction', methods=['POST'])
def make_transaction():
    data = request.json
    sender = data.get('sender')
    recipient = data.get('recipient')
    amount = data.get('amount')
    
    if not sender or not recipient or amount is None:
        return jsonify({'error': 'Sender, recipient, and amount are required'}), 400
    if sender not in users or recipient not in users:
        return jsonify({'error': 'Both sender and recipient must have accounts'}), 404
    if users[sender]['balance'] < amount:
        return jsonify({'error': 'Insufficient funds'}), 400
    
    users[sender]['balance'] -= amount
    users[recipient]['balance'] += amount
    
    return jsonify({'message': 'Transaction successful'}), 200

@app.route("/grant_currency", methods=["POST"])
def grant_currency():
    data = request.json
    username = data.get("username")
    amount = data.get("amount")

    if username not in users:
        return jsonify({"error": "Username not found"}), 404

    if amount <= 0:
        return jsonify({"error": "Grant amount must be positive"}), 400

    users[username]["balance"] += amount
    return jsonify({"message": f"{amount} Budgies granted to {username}. New balance: {users[username]['balance']}"}), 200

# Default route
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to Budgieland Digital Currency API!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
