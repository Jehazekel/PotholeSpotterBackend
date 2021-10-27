from flask import Flask, request, session
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, current_user
from sqlalchemy.exc import IntegrityError, OperationalError
import json

from App.models import *

def getPotholeData():
    #potholes = db.session.query(Pothole).all()
    userAccount = User.query.filter_by().first()

    return json.dumps("test")
    #potholeData = [p.toDict() for p in potholes]
    #return json.dumps(potholeData)