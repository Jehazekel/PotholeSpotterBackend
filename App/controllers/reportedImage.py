#On delete of report, delete reported images.

from flask import Flask, request, session
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, current_user
from sqlalchemy.exc import IntegrityError, OperationalError
import json

from App.models import *
from App.controllers import *


#StackOverflow https://stackoverflow.com/questions/10543940/check-if-a-url-to-an-image-is-up-and-exists-in-python
def is_url_image(image_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    try:
        r = requests.get(image_url)
    except:
        return False
    if r.headers["content-type"] in image_formats:
        return True
    return False

def getPotholeReportImages(reportID):
    if reportID:
        foundReportedImages = db.session.query(ReportedImage).filter_by(reportID=reportID).all()

        if not foundReportedImages:
            return {"error" : "Pothole image not found!"}, 404

        return json.dumps([image.toDict() for image in foundReportedImages]), 200
    else:
        return {"error" : "Invalid pothole image requested!"}, 400

def getIndividualPotholeReportImage(reportID, imageID):
    if reportID and imageID:
        foundReportedImage = db.session.query(ReportedImage).filter_by(imageID=imageID, reportID=reportID).first()

        if not foundReportedImage:
            return {"error" : "Pothole image not found!"}, 404

        return foundReportedImage.toDict(), 200
    else:
        return {"error" : "Invalid pothole image requested!"}, 400

def deletePotholeReportImage(user, potholeID, reportID, imageID):
    if user and reportID and imageID:
        foundReport = db.session.query(Report).filter_by(userID=user.userID, reportID=reportID, potholeID = potholeID).first()

        if not foundReport:
            return {"error" : "You are not the creator of this report!"}, 404

        foundImage = db.session.query(ReportedImage).filter_by(reportID=reportID, imageID=imageID).first()

        if not foundImage:
            return {"error" : "This image does not exist!"}, 404

        try:
            db.session.delete(foundImage)
            db.session.commit()
            return {"message" : "Pothole image succesfully deleted!"}, 200
        except:
            db.session.rollback()
            return {"error" : "Unable to delete report!"}, 500

        
    else:
        return {"error" : "Invalid pothole image submitted!"}, 400


def addPotholeReportImage(user, potholeID, reportID, imageDetails):
    if user and reportID and imageDetails:
        if "images" in imageDetails:
            foundReport = db.session.query(Report).filter_by(userID=user.userID, reportID=reportID, potholeID = potholeID).first()

            if not foundReport:
                return {"error" : "You are not the creator of this report!"}, 404

            invalidCount = 0
            for imageURL in imageDetails["images"]:
                if is_url_image(imageURL):
                    try:
                        reportImage = ReportedImage(reportID=foundReport.reportID, imageURL=imageURL)
                        db.session.add(reportImage)
                        db.session.commit()
                        print("Pothole image succesfully added!")
                    except IntegrityError:
                        db.session.rollback()
                        invalidCount += 1
                        print("Pothole image already exists!")
                    except:
                        invalidCount += 1
                        db.session.rollback()
                        print("Pothole image could not be added.")
            
            if invalidCount > 0:
                return {"error" : "One or more images were not succesfully added."}, 201
            else:
                return {"message" : "All images successfully added."}, 201
        else:
            return {"error" : "Invalid pothole image submitted!"}, 400
    else:
        return {"error" : "Invalid pothole request submitted!"}, 400

