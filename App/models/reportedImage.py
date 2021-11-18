#Justin Baldeosingh
#SpotDPothole-Backend
#NULLIFY

#REPORTEDIMAGE MODEL - Defines the attributes for the reportedImage model, and the relationship between the different tables.

#Imports flask modules and datetime.
from flask_sqlalchemy import SQLAlchemy

#Imports the shared database to be used in defining the model without overwriting the database.
from .sharedDB import db

#Defines the reportedImage database table.
class ReportedImage(db.Model):
    imageID = db.Column(db.Integer, primary_key = True)
    imageURL = db.Column(db.String(200), nullable = False, unique=True)

    #Foreign key that references the report table.
    reportID = db.Column(db.Integer, db.ForeignKey("report.reportID"), nullable=False)

    #Prints the details for a particular reportedImage record.
    def toDict(self):
        return {
            "imageID" : self.imageID,
            "reportID" : self.reportID,
            "imageURL" : self.imageURL,
        }