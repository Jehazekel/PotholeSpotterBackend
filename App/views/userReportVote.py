#Justin Baldeosingh
#SpotDPothole-Backend
#NULLIFY

#USERREPORTVOTE VIEW - Defines the view endpoints for USERREPORTVOTES.

#Imports flask modules.
from flask import Blueprint, redirect, request, jsonify, send_from_directory

#Creates a blueprint to the collection of views for userReportVotes.
userReportVoteViews = Blueprint('userReportVoteViews', __name__)

#Imports the all of the models and controllers of the application.
from App.models import *
from App.controllers import *

#Creates a POST route to facilitate voting on a report. Also returns a status code to denote the outcome of the operation.
@userReportVoteViews.route('/api/vote/pothole/<potholeID>/report/<reportID>/vote', methods=["POST"])
#Ensures that this route is only accessible to logged in users.
@jwt_required()
def voteOnReport(potholeID, reportID):
    voteData = request.get_json()
    outcomeMessage, statusCode = voteOnPothole(current_user, potholeID, reportID, voteData)
    return json.dumps(outcomeMessage), statusCode

#Creates a GET route to retrieve all the votes for a report. Also returns a status code to denote the outcome of the operation.
@userReportVoteViews.route('/api/vote/pothole/<potholeID>/report/<reportID>', methods=["GET"])
def getPotholeVotes(potholeID, reportID):
    voteData = request.get_json()
    displayData, statusCode = getAllVotesForReport(reportID)
    return displayData, statusCode

