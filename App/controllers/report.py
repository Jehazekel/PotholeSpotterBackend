from flask import Flask, request, session
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, current_user
from sqlalchemy.exc import IntegrityError, OperationalError
from geopy import distance
from datetime import datetime, timedelta
import json
import requests

from App.models import *
from App.controllers import *

DISTANCE_THRESHOLD = 20 #Distance in Meters

def getReportData():
    reports = db.session.query(Report).all()
    reportData = [r.toDict() for r in reports]
    return json.dumps(reportData), 200


def reportPotholeStandard(user, reportDetails):
    if "longitude" in reportDetails and "latitude" in reportDetails and "constituencyID" in reportDetails and "description" in reportDetails:
        if -61.965556 < reportDetails["longitude"] < -60.469077 and 10.028088 < reportDetails["latitude"] < 11.370345:
            newPotholeCoords = (reportDetails["latitude"], reportDetails["longitude"])
            finalPothole = None

            smallestDistance = DISTANCE_THRESHOLD

            potholeQuery = db.session.query(Pothole).all()
            for pothole in potholeQuery:
                centerPotholeCoords = (pothole.toDict()["latitude"], pothole.toDict()["longitude"])
                distanceBetweenPotholes = distance.distance(centerPotholeCoords, newPotholeCoords) * 1000
                

                if distanceBetweenPotholes < DISTANCE_THRESHOLD:
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
                newReport = Report(userID = user.userID, potholeID=finalPothole.potholeID, description=reportDetails["description"])
                db.session.add(newReport)
                db.session.commit()

                if "images" in reportDetails:
                    for imageURL in reportDetails["images"]:
                        if is_url_image(imageURL):
                            try:
                                reportImage = ReportedImage(reportID=newReport.reportID, imageURL=imageURL)
                                db.session.add(reportImage)
                                db.session.commit()
                            except:
                                db.session.rollback()
                                print("Unable to add this image to database.")

                try:
                    finalPothole.expiryDate = datetime.now() + timedelta(days=30)
                    db.session.add(finalPothole)
                    db.session.commit()
                except:
                    db.session.rollback()
                    return {"error": "Unable to update expiry date!"}, 500

            except:
                db.session.rollback()
                return {"error": "Unable to add report to database! Ensure that all fields are filled out."}, 500

            return {"message" : "Successfully added pothole report to database!"}, 201

        else:
            return {"error" : "The coordinates are not in Trinidad and Tobago!"}, 400
    else:
        return {"error" : "Invalid report details submitted!"}, 400

def reportPotholeDriver(user, reportDetails):
    if "longitude" in reportDetails and "latitude" in reportDetails and "constituencyID" in reportDetails:
        if -61.965556 < reportDetails["longitude"] < -60.469077 and 10.028088 < reportDetails["latitude"] < 11.370345:
            print("Coordinates in Trinidad and Tobago")
            newPotholeCoords = (reportDetails["latitude"], reportDetails["longitude"])
            finalPothole = None

            smallestDistance = DISTANCE_THRESHOLD

            potholeQuery = db.session.query(Pothole).all()
            for pothole in potholeQuery:
                centerPotholeCoords = (pothole.toDict()["latitude"], pothole.toDict()["longitude"])
                distanceBetweenPotholes = distance.distance(centerPotholeCoords, newPotholeCoords) * 1000
                

                if distanceBetweenPotholes < DISTANCE_THRESHOLD:
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
                newReport = Report(userID = user.userID, potholeID=finalPothole.potholeID, description="Pothole submitted via Driver Mode.")
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

def deletePotholeReport(potholeID, reportID):
        print("Found")
        foundReport = db.session.query(Report).filter_by(potholeID= potholeID, reportID=reportID).first()

        if foundReport:
            
            try:
                db.session.delete(foundReport)
                db.session.commit()

                potholeReports = db.session.query(Report).filter_by(potholeID = potholeID).first()
                if not potholeReports:
                    deletePothole(potholeID)

                return True
            except:
                db.session.rollback()
                return False
        else:
            return False

def deleteUserPotholeReport(user, potholeID, reportID):
    if potholeID and reportID:
        foundReport = db.session.query(Report).filter_by(potholeID=potholeID, reportID=reportID, userID=user.userID).first()

        if foundReport:
            try:
                db.session.delete(foundReport)
                db.session.commit()

                potholeReports = db.session.query(Report).filter_by(potholeID = potholeID).first()
                if not potholeReports:
                    deletePothole(potholeID)
            except:
                db.session.rollback()
                return {"error" : "Unable to delete report."}, 400
            
            return {"error" : "Successfully deleted report."}, 200
        else:
            return {"error" : "Report does not exist! Unable to delete."}, 404
    else:
        return {"error" : "Invalid report details provided."}, 400

    
def updateReportDescription(user, potholeID, reportID, potholeDetails):

    if potholeDetails:
        if "description" in potholeDetails:
            report = db.session.query(Report).filter_by(userID=user.userID, reportID=reportID, potholeID=potholeID).first()
            if report:
                try:
                    report.description = potholeDetails["description"]
                    db.session.add(report)
                    db.session.commit()
                    return {"message" : "Pothole report description updated!"}, 201
                except:
                    db.session.rollback()
                    return {"error": "Unable to update expiry date!"}, 500
            else:
                return {"error" : "Report does not exist!"}, 404
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