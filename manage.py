#Justin Baldeosingh
#SpotDPothole-Backend
#NULLIFY

#Import Modules
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
from datetime import datetime, timedelta

#Imports the main application object and initializes the manager for the application and the database migrator.
from App.main import app
manager = Manager(app)
migrate = Migrate(app, db)

#Sets the migration command for migrating the database.
manager.add_command('db', MigrateCommand)

#Import models and controllers
from App.models import *
from App.controllers import *

#Initializes the database via the 'python3 manage.py initDB' command.
#Creates the database for the application and prints a message once the initialization is complete.
@manager.command
def initDB():
    db.create_all(app=app)
    db.session.commit()
    print('Database Initialized!')

#Defines code that should be run at startup of the server.
def bootstrapServer():
    #Deletes expired potholes.
    deleteExpiredPotholes()

#Allows the flask application to be served via the 'python3 manage.py serve' command.
#Prints the mode in which the application is running, and also serves the application.
@manager.command
def serve():
    print('Application running in ' + app.config['ENV'] + ' mode!')
    #Carries out startup tasks for application server.
    bootstrapServer()
    app.run(host='0.0.0.0', port = 8080, debug = app.config['ENV'] == 'development')


#Allows for the creation of test data via the use of the 'python3 manage.py test' command.
#Modified as needed to test different constructors, interactions, and test cases.
@manager.command
def test():
    pothole1 = Pothole(longitude=-61.277014, latitude=10.626571, constituencyID="arima", expiryDate=datetime.now() + timedelta(days=60))
    db.session.add(pothole1)
    db.session.commit()
    print("test potholes created")    

#If the application is run via 'manage.py', facilitate manager arguments.
if __name__ == "__main__":
    manager.run()

