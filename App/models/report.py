from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from .sharedDB import db

class Report(db.Model):
    reportID = db.Column(db.Integer, primary_key = True)
    userID = db.Column(db.Integer, db.ForeignKey("user.userID"), nullable = False)
    potholeID = db.Column(db.Integer, db.ForeignKey("pothole.potholeID"), nullable=False)
    description = db.Column(db.String(500), nullable = False)
    dateReported = db.Column(db.Date, nullable = False, default=datetime.utcnow)
    votes = db.relationship('UserReportVote', cascade="all, delete", backref='report')
    reportedImages = db.relationship('ReportedImage', cascade="all, delete", backref='report')
    

    def toDict(self):
        return {
            "reportID" : self.reportID,
            "userID" : self.userID,
            "potholeID" : self.potholeID,
            "dateReported" : self.dateReported.strftime("%Y-%m-%d"),
            "description" : self.description,
            "votes" : [vote.toDict() for vote in self.votes],
            "reportedImages" : [rImage.toDict() for rImage in self.reportedImages]
            
        }
