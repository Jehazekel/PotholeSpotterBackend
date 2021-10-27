from flask_script import Manager
from App.main import app
from App.models import db
import os

manager = Manager(app)

from App.models import *

@manager.command
def initDB():
    db.create_all(app=app)
    print('Database Initialized!')

@manager.command
def serve():
    print('Application running in ' + app.config['ENV'] + ' mode!')
    app.run(host='0.0.0.0', port = 8080, debug = app.config['ENV'] == 'development')


@manager.command
def demo():
    user1 = User(username="tester1", firstName="John", lastName="Smith", password = "johnpass123")
    user2 = User(username="tester2", firstName="Johnny", lastName="Steve", password="johnny123")
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    print("test users created")    

if __name__ == "__main__":
    manager.run()