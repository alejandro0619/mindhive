from flask_socketio import Namespace

class Notification(Namespace):
  def on_connect(self):
    print("Connected to the notification channel")

  def on_news(self, data):
    print("New information received: ", data)

class Chat(Namespace):
  def on_connect(self):
    print("Connected to the chat channel!")
  
  def on_message(self, data):
    print("New message:", data)