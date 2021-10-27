from flask import Blueprint, redirect, request, jsonify, send_from_directory

reportViews = Blueprint('reportViews', __name__)

from App.models import *
from App.controllers import *

@reportViews.route('/api/reports', methods=["GET"])
def displayReport():
    displayData = getReportData()
    return displayData