from flask import Flask, request, session
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, current_user
from sqlalchemy.exc import IntegrityError, OperationalError
from geopy import distance
import json

from App.models import *

def getReportData():
    reports = db.session.query(Report).all()
    reportData = [r.toDict() for r in reports]
    return json.dumps(reportData)

def reportPotholeStandard(user, reportDetails):
    '''
    reportID = db.Column(db.Integer, primary_key = True)
    userID = db.Column(db.Integer, db.ForeignKey("user.userID"), nullable = False)
    potholeID = db.Column(db.Integer, db.ForeignKey("pothole.potholeID"), nullable=False)
    description = db.Column(db.String(500), nullable = True)
    dateReported = db.Column(db.Date, nullable = False, default=datetime.utcnow)
    reportedImages = db.relationship('ReportedImage', backref='report')
    '''
    pass

def reportPotholeDriver(user, reportDetails):
    distanceThreshold = 20 #Distance in meters

    if "longitude" in reportDetails and "latitude" in reportDetails and "constituencyID" in reportDetails:

        #print(reportDetails["longitude"])
        #print(reportDetails["latitude"])
        if -61.965556 < reportDetails["longitude"] < -60.469077 and 10.028088 < reportDetails["latitude"] < 11.370345:
            print("Coordinates in Trinidad and Tobago")

            newPotholeCoords = (reportDetails["latitude"], reportDetails["longitude"])
            #print(newPotholeCoords)

            finalPothole = None
            smallestDistance = distanceThreshold

            potholeQuery = db.session.query(Pothole).all()
            for pothole in potholeQuery:
                centerPotholeCoords = (pothole.toDict()["latitude"], pothole.toDict()["longitude"])
                distanceBetweenPotholes = distance.distance(centerPotholeCoords, newPotholeCoords) * 1000
                

                if distanceBetweenPotholes < distanceThreshold:
                    if distanceBetweenPotholes < smallestDistance:
                        finalPothole = pothole

                
            print("Pothole is " + str(distanceBetweenPotholes) + " meters away from nearest pothole within threshold!")   
            print(finalPothole)

            if not finalPothole:
                try:
                    newPothole = Pothole(longitude=reportDetails["longitude"], latitude=reportDetails["latitude"], constituencyID=reportDetails["constituencyID"])
                    db.session.add(newPothole)
                    db.session.commit()
                    finalPothole = newPothole
                except:
                    db.session.rollback()
                    return {"error": "Error adding pothole to database!"}

            alreadySubmitted = db.session.query(Report).filter_by(userID=user.userID, potholeID=finalPothole.potholeID).first()
            if alreadySubmitted:
                return {"error" : "You have already reported this pothole!"}

            try:
                newReport = Report(userID = user.userID, potholeID=finalPothole.potholeID)
                db.session.add(newReport)
                db.session.commit()
            except:
                db.session.rollback()
                return {"error": "Unable to add report to database!"}

            return {"message" : "Successfully added pothole report to database!"}

        else:
            return {"error" : "The coordinates are not in Trinidad and Tobago!"}
    else:
        return {"error" : "Invalid report details submitted!"}