from flask import Flask, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, current_user
from datetime import timedelta 
from sqlalchemy.exc import IntegrityError, OperationalError
import json

from App.models import *
from App.views import *

def loadConfig(app):
    #try to load config from file, if fails then try to load from environment
    try:
        app.config.from_object('App.config.development')
        #app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri() if app.config['SQLITEDB'] else app.config['DBURI']
    except:
        print("config file not present using environment variables")

def create_app():
    app = Flask(__name__)
    loadConfig(app)
    db.init_app(app)
    return app

app = create_app()
app.app_context().push()
jwt = JWTManager(app)

#app.register_blueprint(api_views)
app.register_blueprint(userViews)


'''AUTH'''
# Register a callback function that loades a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()

'''AUTH'''