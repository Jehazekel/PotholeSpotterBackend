from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from .sharedDB import db

class User(db.Model):
    userID = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique = True)
    firstName = db.Column(db.String(64), nullable = False)
    lastName = db.Column(db.String(64), nullable = False)
    password = db.Column(db.String(256), nullable = False)
    reports = db.relationship('Report', cascade="all, delete", backref='user')
    votes = db.relationship('UserReportVote', cascade="all, delete", backref='voter')

    def __init__(self, email, firstName, lastName, password):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.setPassword(password)

    def setPassword(self, password):
        self.password = generate_password_hash(password, method='sha256')
    
    def checkPassword(self, password):
        return check_password_hash(self.password, password)

    def toDict(self):
        return {
            "userID" : self.userID,
            "email" : self.email,
            "firstName" : self.firstName,
            "lastName" : self.lastName,
            "password" : self.password
        }
    