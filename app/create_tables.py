from app import connection

try:

    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL  
                );"""
        )

except Exception as ex:
    print("[INFO] Error while working with PostgreSQL", ex)
