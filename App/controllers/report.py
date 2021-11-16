from flask import Flask, request, session
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, current_user
from sqlalchemy.exc import IntegrityError, OperationalError
from geopy import distance
from datetime import datetime, timedelta
import json

from App.models import *

def getReportData():
    reports = db.session.query(Report).all()
    reportData = [r.toDict() for r in reports]
    return json.dumps(reportData), 200

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
        if -61.965556 < reportDetails["longitude"] < -60.469077 and 10.028088 < reportDetails["latitude"] < 11.370345:
            print("Coordinates in Trinidad and Tobago")
            newPotholeCoords = (reportDetails["latitude"], reportDetails["longitude"])
            finalPothole = None

            smallestDistance = distanceThreshold

            potholeQuery = db.session.query(Pothole).all()
            for pothole in potholeQuery:
                centerPotholeCoords = (pothole.toDict()["latitude"], pothole.toDict()["longitude"])
                distanceBetweenPotholes = distance.distance(centerPotholeCoords, newPotholeCoords) * 1000
                

                if distanceBetweenPotholes < distanceThreshold:
                    if distanceBetweenPotholes < smallestDistance:
                        finalPothole = pothole

            if not finalPothole:
                try:
                    newPothole = Pothole(longitude=reportDetails["longitude"], latitude=reportDetails["latitude"], constituencyID=reportDetails["constituencyID"], expiryDate=datetime.now() + timedelta(days=60))
                    db.session.add(newPothole)
                    db.session.commit()
                    finalPothole = newPothole
                except:
                    db.session.rollback()
                    return {"error": "Error adding pothole to database!"}, 500
            else:
                alreadySubmitted = db.session.query(Report).filter_by(userID=user.userID, potholeID=finalPothole.potholeID).first()
                if alreadySubmitted:
                    try:
                        finalPothole.expiryDate = datetime.now() + timedelta(days=30)
                        db.session.add(finalPothole)
                        db.session.commit()
                        return {"message" : "Expiry date of pothole has been reset!"}, 201
                    except:
                        db.session.rollback()
                        return {"error": "Unable to update expiry date!"}, 500
            try:
                newReport = Report(userID = user.userID, potholeID=finalPothole.potholeID)
                db.session.add(newReport)
                db.session.commit()

                try:
                    finalPothole.expiryDate = datetime.now() + timedelta(days=30)
                    db.session.add(finalPothole)
                    db.session.commit()
                except:
                    db.session.rollback()
                    return {"error": "Unable to update expiry date!"}, 500

            except:
                db.session.rollback()
                return {"error": "Unable to add report to database!"}, 500

            return {"message" : "Successfully added pothole report to database!"}, 201

        else:
            return {"error" : "The coordinates are not in Trinidad and Tobago!"}, 400
    else:
        return {"error" : "Invalid report details submitted!"}, 400


def getPotholeReports(potholeID):
    reports = db.session.query(Report).filter_by(potholeID=potholeID).all()
    reportData = [r.toDict() for r in reports]
    return json.dumps(reportData), 200

def getIndividualPotholeReport(potholeID, reportID):
    report = db.session.query(Report).filter_by(potholeID=potholeID, reportID=reportID).first()
    if(report):
        return json.dumps(report.toDict()), 200
    else:
        return json.dumps({"error": "No report found."}), 404