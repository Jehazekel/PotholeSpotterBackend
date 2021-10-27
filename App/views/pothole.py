from flask import Blueprint, redirect, request, jsonify, send_from_directory

potholeViews = Blueprint('potholeViews', __name__)

from App.models import *
from App.controllers import *

@potholeViews.route('/api/potholes', methods=["GET"])
def displayPotholes():
    displayData = getPotholeData()
    return displayData