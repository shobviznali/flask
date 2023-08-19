from flask import Flask
import psycopg2


db_params = {
    "host": "127.0.0.1",
    "database": "flask_users",
    "user": "postgres",
    "password": "1234"
}
app = Flask(__name__)
connection = psycopg2.connect(**db_params)

from app import routes
