import os

# MongoDB Configuration
MONGO_URI = "mongodb+srv://admin:adminpassword@cluster0.464wvua.mongodb.net/"

# MySQL Configuration
MYSQL_DATABASE_HOST = 'sqldb.cr0gumy26ddi.us-west-2.rds.amazonaws.com'
MYSQL_DATABASE_DB = 'sqldb'
MYSQL_DATABASE_USER = os.getenv('admin')
MYSQL_DATABASE_PASSWORD = os.getenv('adminpassword')
MYSQL_DATABASE_PORT = 3306
