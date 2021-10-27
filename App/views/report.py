from flask import Blueprint, redirect, request, jsonify, send_from_directory

reportViews = Blueprint('reportViews', __name__)

from App.models import *
from App.controllers import *