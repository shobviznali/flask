from flask import Flask
import psycopg2
import socket
from flask_socketio import SocketIO, emit

db_params = {
    "host": "127.0.0.1",
    "database": "flask_users",
    "user": "postgres",
    "password": "1234"
}

app = Flask(__name__)
app.secret_key = "secret"
connection = psycopg2.connect(**db_params)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

websocket = SocketIO(app)

from app import routes
