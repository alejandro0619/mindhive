from flask import Flask
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, emit

from routes.auth import auth_bp
from routes.user import user_bp
from wb import Chat, Notification

# Config:
from config import Config

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
    socket = SocketIO(app, manage_session = False)
    app.config.socket = socket
    socket.run()
    # Register the websocket namespaces
    socket.on_namespace(Notification('/notification'))
    socket.on_namespace(Chat('/chat'))
