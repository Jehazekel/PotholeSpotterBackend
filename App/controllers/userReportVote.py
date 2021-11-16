from flask import Flask, request, session
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, current_user
from sqlalchemy.exc import IntegrityError, OperationalError
from geopy import distance
from datetime import datetime, timedelta
import json

from App.models import *
from App.controllers import *

REPORT_DELETION_THRESHOLD = -1

def getAllVotesForReport(reportID):
    votes = db.session.query(UserReportVote).all()
    voteData = [v.toDict() for v in votes]
    return json.dumps(voteData), 200

def getAllUpvotesForReport(reportID):
    upvotes = db.session.query(UserReportVote).filter_by(reportID=reportID, upvote=True).all()
    upvoteData = [uv.toDict() for uv in upvotes]
    return json.dumps(upvoteData), 200


def getAllDownvotesForReport(reportID):
    downvotes = db.session.query(UserReportVote).filter_by(reportID=reportID, upvote=False).all()
    downvoteData = [dv.toDict() for dv in downvotes]
    return json.dumps(downvoteData), 200

def voteOnPothole(user, potholeID, reportID, voteData):
    if not voteData:
        return {"error": "No vote data supplied."}, 400

    if "upvote" not in voteData:
        return {"error": "Invalid vote request submitted"}, 400

    report = db.session.query(Report).filter_by(potholeID=potholeID, reportID=reportID).first()

    if(report):
        existingVote = db.session.query(UserReportVote).filter_by(userID=user.userID, reportID=reportID).first()
        
        if voteData["upvote"] == False or voteData["upvote"] == True:
            try:
                if not existingVote: 
                    newVote = UserReportVote(reportID = reportID, upvote = voteData["upvote"], userID = user.userID)
                    db.session.add(newVote)
                    db.session.commit()

                    if calculateNetVotes(reportID) <= REPORT_DELETION_THRESHOLD:
                        deletePotholeReport(potholeID, reportID)
                        return {"message": "This report will be deleted due to its severe negative reputation."}, 200

                    return {"message": "Vote casted for report!"}, 201
                else:
                    if existingVote.upvote == voteData["upvote"]:
                        db.session.delete(existingVote)
                        db.session.commit()
                        return {"message": "Vote removed from report!"}, 200
                    else:
                        existingVote.upvote = voteData["upvote"]
                        db.session.add(existingVote)
                        db.session.commit()

                        if calculateNetVotes(reportID) <= REPORT_DELETION_THRESHOLD:
                            deletePotholeReport(potholeID, reportID)
                            return {"message": "This report will be deleted due to its severe negative reputation."}, 200

                        return {"message": "Vote updated for report!"}, 200
            except :
                db.session.rollback();
                return {"error": "Error voting for this report!"}, 500
        else:
            return {"error": "Invalid vote data supplied!"}, 400
    else:
        return {"error": "No report found."}, 404

def calculateNetVotes(reportID):
    upvotes = db.session.query(UserReportVote).filter_by(reportID=reportID, upvote=True).count()
    downvotes = db.session.query(UserReportVote).filter_by(reportID=reportID, upvote=False).count()
    print(upvotes-downvotes)
    return (upvotes-downvotes)