from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ReportedImage(db.Model):
    imageID = db.Column(db.Integer, primary_key = True)
    #reportID
    imageURL = db.Column(db.String(200), nullable = False)

    def toDict(self):
        return {
            "reportID" : self.reportID,
            "userID" : self.userID,
            "potholeID" : self.potholeID,
            "dateReported" : self.dateReported,
            "description" : self.description,
            "reportedImages" : self.imageURL
        }