from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Database setup
DATABASE_URL = "sqlite:///budgieland.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# User model
class User(Base):
    __tablename__ = "users"
    idn = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0)

Base.metadata.create_all(bind=engine)

# Routes
@app.route("/create_account", methods=["POST"])
def create_account():
    data = request.json
    username = data.get("username")
    if session.query(User).filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    new_user = User(username=username, balance=0)
    session.add(new_user)
    session.commit()
    return jsonify({"message": f"Account created for {username}"}), 201

@app.route("/check_balance", methods=["GET"])
def check_balance():
    username = request.args.get("username")
    user = session.query(User).filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Username not found"}), 404
    return jsonify({"username": username, "balance": user.balance})

@app.route("/make_transaction", methods=["POST"])
def make_transaction():
    data = request.json
    sender_name = data.get("sender")
    recipient_name = data.get("recipient")
    amount = data.get("amount")

    sender = session.query(User).filter_by(username=sender_name).first()
    recipient = session.query(User).filter_by(username=recipient_name).first()

    if not sender or not recipient:
        return jsonify({"error": "Both sender and recipient must have accounts"}), 404

    if sender.balance < amount:
        return jsonify({"error": "Insufficient funds"}), 400

    sender.balance -= amount
    recipient.balance += amount
    session.commit()
    return jsonify({"message": f"Transaction complete: {amount} Budgies from {sender_name} to {recipient_name}"}), 200

@app.route("/grant_currency", methods=["POST"])
def grant_currency():
    data = request.json
    username = data.get("username")
    amount = data.get("amount")

    user = session.query(User).filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Username not found"}), 404

    if amount <= 0:
        return jsonify({"error": "Grant amount must be positive"}), 400

    user.balance += amount
    session.commit()
    return jsonify({"message": f"{amount} Budgies granted to {username}. New balance: {user.balance}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
