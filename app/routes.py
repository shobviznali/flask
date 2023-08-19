from flask import render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from app import connection

@app.route('/')
def home():
    return render_template("index.html", content="Home page")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT password FROM users WHERE username = %s""", (username,))
            hash = cursor.fetchone()

            if hash:
                if check_password_hash(hash[0], password):

                    return "Login is successfully"
                else:
                    return "Try again"

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        insert_query = "INSERT INTO users (username, password) VALUES (%s, %s);"
        with connection.cursor() as cursor:
            cursor.execute(insert_query, (username, hashed_password))
            connection.commit()
        return "User registered successfully"
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template("about.html")


content_mes = "This is telephone number you can contact us \n +37455977780"
@app.route('/faq')
def faq():
    return render_template("faq.html", title="FAQ", content=content_mes)

