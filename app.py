from flask import Flask
from flask_mysqldb import MySQL
from flask_mail import Mail, Message

from routes.auth import auth_bp
from routes.user import user_bp

# Config:
from config import Config
# from lib.queue_message import messages

# Factory dispatches an instance of the app
def make_app():
    app = Flask(__name__)
    config = Config() # Build an instance of
    config.MYSQL = MySQL(app)
    app.config.from_object(config)

    
    

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    return app


if __name__ == '__main__':
    app = make_app()
    app.run()
    
    
