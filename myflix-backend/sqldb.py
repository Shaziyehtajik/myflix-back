from flask import current_app, g, jsonify
from werkzeug.local import LocalProxy
import pymysql
import bcrypt

def get_sqldb():
    if 'sqldb' not in g:
        g.sqldb = pymysql.connect(
            host=current_app.config.get('MYSQL_DATABASE_HOST'),
            user=current_app.config.get('MYSQL_DATABASE_USER'),
            password=current_app.config.get('MYSQL_DATABASE_PASSWORD'),
            database=current_app.config.get('MYSQL_DATABASE_DB'),
            port=3306
        )
    return g.sqldb

# Use LocalProxy to read the global db instance with just `db`
sqldb = LocalProxy(get_sqldb)

# User Management

def register_user(username, password):
    with sqldb.cursor() as cursor:
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        values = (username, str(hashed_pwd, 'utf-8'))
        result = cursor.execute(sql, values)
        sqldb.commit()
        return result == 1

def authenticate_user(username, password):
    with sqldb.cursor() as cursor:
        sql = "SELECT * FROM users WHERE username=%s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password.encode('utf-8'), result[2].encode('utf-8')):
            return result[0]  # Return user ID as token
        return None

def update_user_profile(username, new_password):
    with sqldb.cursor() as cursor:
        hashed_pwd = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt(10))
        sql = "UPDATE users SET password=%s WHERE username=%s"
        values = (str(hashed_pwd, 'utf-8'), username)
        result = cursor.execute(sql, values)
        sqldb.commit()
        return result == 1

# Additional functions for user movie interactions, admin functionalities, etc.

def verify(username, password):
    with sqldb.cursor() as cursor:
        sql = "SELECT * FROM login WHERE username=%s"
        cursor.execute(sql, (username,))
        results = cursor.fetchone()

        entered_password = password.encode('utf-8')

        if results and bcrypt.checkpw(entered_password, results[2].encode('utf-8')):
            return True
        else:
            return False

def create(username, password):
    with sqldb.cursor() as cursor:
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))
        sql = "INSERT INTO login (username, pass) VALUES (%s, %s)"
        values = (username, str(hashed_pwd, 'utf-8'))
        result = cursor.execute(sql, values)
        sqldb.commit()
        return result == 1
