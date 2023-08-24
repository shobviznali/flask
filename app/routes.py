from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, websocket
from app import connection
from app import password_check
from flask_socketio import emit

@app.route('/')
def home():
    return render_template("index.html", content="Home page")


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        new_password = request.form['new_password']
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT password FROM users WHERE username = %s""", (username,))
            hash = cursor.fetchone()

            update_query = "UPDATE users SET password = %s WHERE username = %s"

            if not check_password_hash(hash[0], password):
                connection.commit()
                return "Wrong password"
            else:
                hashed_password = generate_password_hash(new_password, method='sha256')
                cursor.execute(update_query, (hashed_password, username))
                connection.commit()
                return "Password updated"
    return render_template('edit.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT password FROM users WHERE username = %s""", (username,))
            hash = cursor.fetchone()
            true = True
            if hash:
                if check_password_hash(hash[0], password):
                    connection.commit()
                    session.get("username")
                    cursor.execute(f"""UPDATE users SET is_logged_in = %s WHERE username = %s""", (true, username,))
                    session["username"] = username
                    return render_template('index.html')
                else:
                    connection.commit()
                    return "Try again"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        insert_query = "INSERT INTO users (username, password) VALUES (%s, %s);"

        if not password_check.is_strong_password(password):
            return "Your password is not strong enough"
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(insert_query, (username, hashed_password))
                    connection.commit()
                    return "User registered successfully"
            except Exception as ex:
                connection.commit()
                return render_template('register.html')





    return render_template('register.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        delete_query = "DELETE FROM users WHERE username = %s"
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT password FROM users WHERE username = %s""", (username,))
            hash = cursor.fetchone()

            if hash:
                if check_password_hash(hash[0], str(password)):
                    cursor.execute(delete_query, (username,))
                    connection.commit()
                    return "Deleted"
                else:
                    connection.commit()
                    return "Try again"
    return render_template('delete_user.html')



@app.route('/about')
def about():
    return render_template("about.html")


content_mes = "This is telephone number you can contact us \n +37455977780"
@app.route('/faq')
def faq():
    return render_template("faq.html", title="FAQ", content=content_mes)


@app.route('/chat', methods=['GET', 'POST'] )
def view():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, username FROM users")
        users = cursor.fetchall()
        print(users)

        for i in range(len(users)):
            if session.get('username') in users[i]:
                sender_id = users[i][0]

        message = request.form.get("message")

        selected_user = request.form.get("selected_user")

        print(message)

    return render_template('chat.html', users=users)
