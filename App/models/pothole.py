from flask_sqlalchemy import SQLAlchemy

from .sharedDB import db

class Pothole(db.Model):
    potholeID = db.Column(db.Integer, primary_key = True)
    longitude = db.Column(db.Float, nullable = False)
    latitude = db.Column(db.Float, nullable = False)
    constituencyID = db.Column(db.String(100), nullable = False)
    expiryDate = db.Column(db.Date, nullable = False)
    reports = db.relationship('Report', cascade="all, delete", backref='pothole')

    def toDict(self):
        return {
            "potholeID" : self.potholeID,
            "longitude" : self.longitude,
            "latitude" : self.latitude,
            "constituencyID" : self.constituencyID,
            "expiryDate" : self.expiryDate.strftime("%Y-%m-%d")
        }
    