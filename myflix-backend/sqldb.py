from flask import current_app, g
from werkzeug.local import LocalProxy
import pymysql
from bson.json_util import dumps
import bcrypt

def get_sqldb():
    if 'sqldb' not in g:
        g.sqldb = pymysql.connect(
            host='sqldb.cr0gumy26ddi.us-west-2.rds.amazonaws.com',
            user=current_app.config.get('admin'),
            password=current_app.config.get('adminpassword'),
            database=current_app.config.get('sqldb'),
            port=3306
        )
    return g.sqldb

# Use LocalProxy to read the global db instance with just `db`
sqldb = LocalProxy(get_sqldb)

# User Management

def register_user(username, password):
    with sqldb.cursor() as cursor:
        password = password.encode('utf-8')
        hashed_pwd = bcrypt.hashpw(password, bcrypt.gensalt(10)) 
        
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        values = (username, str(hashed_pwd, 'utf-8'))
        result = cursor.execute(sql, values)

        # Committing the change to the DB
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
        new_password = new_password.encode('utf-8')
        hashed_pwd = bcrypt.hashpw(new_password, bcrypt.gensalt(10))
        
        sql = "UPDATE users SET password=%s WHERE username=%s"
        values = (str(hashed_pwd, 'utf-8'), username)
        result = cursor.execute(sql, values)

        # Committing the change to the DB
        sqldb.commit()
        return result == 1

# ... (Add more functions for user movie interactions, admin functionalities, etc.)
