from flask import Flask, request, session
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, current_user
from sqlalchemy.exc import IntegrityError, OperationalError
import json

from App.models import *

def identity(payload):
  return db.session.query(User).get(payload['identity'])

def authenticate(username, password):
    user = User.filter_by(username=username).first()
    if user and user.checkPassword(password):
        return user

def registerUserController(regData):  
    if regData:
        if "username" in regData and "firstName" in regData and "lastName" in regData and "password" in regData and "confirmPassword" in regData:
            parsedUsername = regData["username"].replace(" ", "")
            parsedFirstName = regData["firstName"].replace(" ", "")
            parsedLastName = regData["lastName"].replace(" ", "")

            if len(parsedFirstName) < 2:
                return {"error" : "First name is invalid!"}
            
            if len(parsedLastName) < 2:
                return {"error": "Last name is invalid!"}

            if len(regData["password"]) < 6:
                return {"error": "Password is too short"}
            
            if regData["password"] != regData["confirmPassword"]:
                return {"error" : "Passwords do not match!"}

            try:
                newUser = User(parsedUsername, parsedFirstName, parsedLastName, regData["password"])
                db.session.add(newUser)
                db.session.commit()
                return {"message" : "Sucesssfully registered!"}
            except IntegrityError:
                db.session.rollback()
                return {"error" : "User already exists!"}
            except OperationalError:
                print("Database not initialized!")
                return {"error" : "Database not initialized! Contact the administrator of the application!"}
            except:
                return {"error" : "An unknown error has occurred!"}
            
    return {"error" : "Invalid registration details provided!"}


def loginUserController(loginDetails):  
    if loginDetails:
        if "username" in loginDetails and "password" in loginDetails:
            userAccount = User.query.filter_by(username=loginDetails["username"]).first()
            
            if not userAccount or not userAccount.checkPassword(loginDetails["password"]):
                return {"error" : "Wrong username or password entered!"}

            if userAccount and userAccount.checkPassword(loginDetails["password"]):
                access_token = create_access_token(identity = loginDetails["username"])
                return {"access_token" : access_token}

    return {"error" : "Invalid login details provided!"}

def identifyUser(current_user):
    if current_user:
        return {"username" : current_user.username, "firstName" : current_user.firstName, "lastName": current_user.lastName}
    
    return json.dumps({"error" : "User is not logged in!"})