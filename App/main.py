#Justin Baldeosingh
#SpotDPothole-Backend
#NULLIFY

#Import Modules
from flask import Flask, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, current_user
import os

#Imports the models and views of the application.
from App.models import *
from App.views import *

#Loads the configuration into the application from either a config file, or using environment variables.
def loadConfig(app):
    #Attempts to configure the application from a configuration file.
    try:
        app.config.from_object('App.config.development')
    except:
    #If no configuration file is present, use the environment variables of the host to configure the application.
        print("Config file not present. Using environment variables.")
        app.config['ENV'] = os.environ.get('ENV', 'development')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['JWT_EXPIRATION_DELTA'] = os.environ.get('JWT_EXPIRATION_DELTA')
        app.config['DEBUG'] = os.environ.get('DEBUG')
        app.config['ENV'] = os.environ.get('ENV')

#Creates the application, loads the configuration, initializes the database, and returns the application context.
def create_app():
    app = Flask(__name__)
    loadConfig(app)
    db.init_app(app)
    return app

#Creates the application object.
app = create_app()
app.app_context().push()

#Creates the manager for the application, for the JSON web tokens using in authentication.
jwt = JWTManager(app)

#Registers the different view blueprints for the different API endpoints.
app.register_blueprint(potholeViews)
app.register_blueprint(userViews)
app.register_blueprint(reportedImageViews)
app.register_blueprint(reportViews)
app.register_blueprint(userReportVoteViews)


# Flask Boilerplate for loading a user's context.
# Register a callback function that loades a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(email=identity).one_or_none()