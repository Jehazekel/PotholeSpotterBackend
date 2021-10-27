from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from .sharedDB import db

class Report(db.Model):
    reportID = db.Column(db.Integer, primary_key = True)
    userID = db.Column(db.Integer, db.ForeignKey("user.userID"), nullable = False)
    potholeID = db.Column(db.Integer, db.ForeignKey("pothole.potholeID"), nullable=False)
    description = db.Column(db.String(500), nullable = True)
    dateReported = db.Column(db.Date, nullable = False, default=datetime.utcnow)
    reportedImages = db.relationship('ReportedImage', backref='report')
    

    def toDict(self):
        return {
            "reportID" : self.reportID,
            "userID" : self.userID,
            "potholeID" : self.potholeID,
            "dateReported" : self.dateReported,
            "description" : self.description,
            "reportedImages" : [rImage.toDict() for rImage in reportedImages]
        }