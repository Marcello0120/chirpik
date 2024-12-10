import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Your routes and logic here

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
