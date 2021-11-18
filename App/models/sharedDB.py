#Imports the Flask SQLAlchemy Database Module
from flask_sqlalchemy import SQLAlchemy

#Creates a new database object to be used throughout all of the models for the application.
db = SQLAlchemy()