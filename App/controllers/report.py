from flask import Flask, request, session
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, current_user
from sqlalchemy.exc import IntegrityError, OperationalError
import json

from App.models import *

def getReportData():
    reports = db.session.query(Report).all()
    reportData = [r.toDict() for r in reports]
    return json.dumps(reportData)