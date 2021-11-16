from flask import Blueprint, redirect, request, jsonify, send_from_directory

potholeViews = Blueprint('potholeViews', __name__)

from App.models import *
from App.controllers import *

@potholeViews.route('/api/potholes', methods=["GET"])
def displayPotholes():
    displayData, statusCode = getPotholeData()
    return displayData, statusCode

@potholeViews.route('/api/potholes/<id>', methods=["GET"])
def displayIndividualPotholes(id):
    displayData, statusCode = getIndividualPotholeData(id)
    return displayData, statusCode