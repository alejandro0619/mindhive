from flask_mysqldb import MySQL
from flask import current_app
from platform import os

class Config:
    SECRET_KEY = 'arremangala arrepujala sí, arremangala arrepujala no'
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'mindhive'
    MYSQL_UNIX_SOCKET = None
    MYSQL = None
    def __init__(self):
        if os.name != 'nt':
            self.MYSQL_UNIX_SOCKET = '/opt/lampp/var/mysql/mysql.sock'
        else:
            self.MYSQL_UNIX_SOCKET = None