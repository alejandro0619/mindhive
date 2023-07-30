from platform import os
from flask_mail import Mail, Message

class Config:
    SECRET_KEY = 'arremangala arrepujala sí, arremangala arrepujala no'
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'mindhive'
    MYSQL_UNIX_SOCKET = None
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'mindhive025@gmail.com'
    MAIL_PASSWORD = 'hcmhifzbldtgdwat'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    def __init__(self):
        if os.name != 'nt':
            self.MYSQL_UNIX_SOCKET = '/opt/lampp/var/mysql/mysql.sock'