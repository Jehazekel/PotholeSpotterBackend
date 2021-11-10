from flask import Flask, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, current_user
from datetime import timedelta 
from sqlalchemy.exc import IntegrityError, OperationalError
import json, os

from App.models import Pothole, User, Report, ReportedImage, db
from App.views import *

def loadConfig(app):
    app.config['ENV'] = os.environ.get('ENV', 'development')
    try:
        app.config.from_object('App.config.development')
    except:
        print("config file not present using environment variables")
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['JWT_EXPIRATION_DELTA'] = os.environ.get('JWT_EXPIRATION_DELTA')
        app.config['DEBUG'] = os.environ.get('DEBUG')
        app.config['ENV'] = os.environ.get('ENV')

def create_app():
    app = Flask(__name__)
    loadConfig(app)
    db.init_app(app)
    return app

app = create_app()
app.app_context().push()
jwt = JWTManager(app)

app.register_blueprint(potholeViews)
app.register_blueprint(userViews)
app.register_blueprint(reportedImageViews)
app.register_blueprint(reportViews)



'''AUTH'''
# Register a callback function that loades a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(email=identity).one_or_none()

'''AUTH'''