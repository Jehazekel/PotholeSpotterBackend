from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Report(db.Model):
    reportID = db.Column(db.Integer, primary_key = True)
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    #potholeID {FK}
    description = db.Column(db.String(500), nullable = True)
    dateReported = db.Column(db.Date, nullable = False)
    reportedImages = db.relationship('ReportedImage', backref='report')
    

    def toDict(self):
        return {
            "reportID" : self.reportID,
            "userID" : self.userID,
            "potholeID" : self.potholeID,
            "dateReported" : self.dateReported,
            "description" : self.description,
            "reportedImages" : self.imageURL
        }