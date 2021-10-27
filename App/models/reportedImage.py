from flask_sqlalchemy import SQLAlchemy

from .sharedDB import db

class ReportedImage(db.Model):
    imageID = db.Column(db.Integer, primary_key = True)
    reportID = db.Column(db.Integer, db.ForeignKey("report.reportID"), nullable=False)
    imageURL = db.Column(db.String(200), nullable = False)

    def toDict(self):
        return {
            "imageID" : self.imageID,
            "reportID" : self.reportID,
            "imageURL" : self.imageURL,
        }