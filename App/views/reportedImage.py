from flask import Blueprint, redirect, request, jsonify, send_from_directory

reportedImageViews = Blueprint('reportedImageViews', __name__)

from App.models import *
from App.controllers import *