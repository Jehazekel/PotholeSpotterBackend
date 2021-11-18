#Justin Baldeosingh
#SpotDPothole-Backend
#NULLIFY

#USERREPORTVOTE MODEL - Defines the attributes for the userReportVote model, and the relationship between the different tables.

#Imports flask modules and datetime.
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Imports the shared database to be used in defining the model without overwriting the database.
from .sharedDB import db

#Defines the UserReportVote database table.
class UserReportVote(db.Model):
    voteID = db.Column(db.Integer, primary_key = True)
    upvote = db.Column(db.Boolean, nullable = False)

    #Foreign key that references the user table.
    userID = db.Column(db.Integer, db.ForeignKey("user.userID"), nullable = False)
    #Foreign key that references the report table.
    reportID = db.Column(db.Integer, db.ForeignKey("report.reportID"), nullable=False)
    
    #Prints the details for a particular UserReportVote record.
    def toDict(self):
        return {
            "voteID" : self.voteID,
            "userID" : self.userID,
            "reportID" : self.reportID,
            "upvote" : self.upvote,
        }