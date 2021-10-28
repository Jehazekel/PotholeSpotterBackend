from flask_script import Manager
from App.main import app
import os
from datetime import datetime, timedelta
manager = Manager(app)

from App.models import Pothole, User, Report, ReportedImage, db

@manager.command
def initDB():
    db.create_all(app=app)
    db.session.commit()
    print('Database Initialized!')

@manager.command
def serve():
    print('Application running in ' + app.config['ENV'] + ' mode!')
    app.run(host='0.0.0.0', port = 8080, debug = app.config['ENV'] == 'development')


@manager.command
def demo():
    pothole1 = Pothole(longitude=-61.277014, latitude=10.626571, constituencyID="arima", expiryDate=datetime.now() + timedelta(days=60))
    db.session.add(pothole1)
    db.session.commit()
    print("test potholes created")    

if __name__ == "__main__":
    manager.run()