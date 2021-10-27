from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from .sharedDB import db

class User(db.Model):
    userID = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    firstName = db.Column(db.String(64), nullable = False)
    lastName = db.Column(db.String(64), nullable = False)
    password = db.Column(db.String(256), nullable = False)
    reports = db.relationship('Report', backref='user')

    def __init__(self, username, firstName, lastName, password):
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.setPassword(password)

    def setPassword(self, password):
        self.password = generate_password_hash(password, method='sha256')
    
    def checkPassword(self, password):
        return check_password_hash(self.password, password)

    def reportPotholeStandard():
        pass
    
    def reportPotholeDriver():
        pass

    def toDict(self):
        return {
            "userID" : self.userID,
            "username" : self.username,
            "firstName" : self.firstName,
            "lastName" : self.lastName,
            "password" : self.password
        }
    