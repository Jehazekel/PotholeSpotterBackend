from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from .sharedDB import db

class UserReportVote(db.Model):
    voteID = db.Column(db.Integer, primary_key = True)
    userID = db.Column(db.Integer, db.ForeignKey("user.userID"), nullable = False)
    reportID = db.Column(db.Integer, db.ForeignKey("report.reportID"), nullable=False)
    upvote = db.Column(db.Boolean, nullable = False)
    

    def toDict(self):
        return {
            "voteID" : self.voteID,
            "userID" : self.userID,
            "reportID" : self.reportID,
            "upvote" : self.upvote,
        }