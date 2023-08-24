from app import connection

try:

    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,  
                is_logged_in BOOL
                );"""
        )

    with connection.cursor() as curosr2:
        curosr2.execute(

        """CREATE TABLE IF NOT EXISTS users(
               id INT PRIMARY KEY,
                sender_id INT,
                receiver_id INT,
                message TEXT  
                );"""
        )

    with connection.cursor() as curosr3:
        curosr3.execute(
            """
           CREATE TABLE IF NOT EXISTS status(
               user_id INT PRIMARY KEY,
                status VARCHAR(10)
              );"""
        )

except Exception as ex:
    print("[INFO] Error while working with PostgreSQL", ex)
