from flask import Flask, request, session
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, current_user
from sqlalchemy.exc import IntegrityError, OperationalError
import json

from App.models import *

def identity(payload):
  return db.session.query(User).get(payload['identity'])

def authenticate(email, password):
    user = User.filter_by(email=email).first()
    if user and user.checkPassword(password):
        return user

def registerUserController(regData):  
    if regData:
        if "email" in regData and "firstName" in regData and "lastName" in regData and "password" in regData and "confirmPassword" in regData:
            parsedEmail = regData["email"].replace(" ", "")
            parsedFirstName = regData["firstName"].replace(" ", "")
            parsedLastName = regData["lastName"].replace(" ", "")

            if len(parsedEmail) < 3 or not "@" in parsedEmail or not "." in parsedEmail:
                return {"error" : "Email is invalid!"}, 400

            if len(parsedFirstName) < 2:
                return {"error" : "First name is invalid!"}, 400
            
            if len(parsedLastName) < 2:
                return {"error": "Last name is invalid!"}, 400

            if len(regData["password"]) < 6:
                return {"error": "Password is too short"}, 400
            
            if regData["password"] != regData["confirmPassword"]:
                return {"error" : "Passwords do not match!"}, 400

            try:
                newUser = User(parsedEmail, parsedFirstName, parsedLastName, regData["password"])
                db.session.add(newUser)
                db.session.commit()
                return {"message" : "Sucesssfully registered!"}, 201
            except IntegrityError:
                db.session.rollback()
                return {"error" : "User already exists!"}, 409
            except OperationalError:
                print("Database not initialized!")
                return {"error" : "Database not initialized! Contact the administrator of the application!"}, 500
            except:
                return {"error" : "An unknown error has occurred!"}, 500
            
    return {"error" : "Invalid registration details provided!"}, 400


def loginUserController(loginDetails):  
    if loginDetails:
        if "email" in loginDetails and "password" in loginDetails:
            userAccount = User.query.filter_by(email=loginDetails["email"]).first()
            
            if not userAccount or not userAccount.checkPassword(loginDetails["password"]):
                return {"error" : "Wrong email or password entered!"}, 401

            if userAccount and userAccount.checkPassword(loginDetails["password"]):
                access_token = create_access_token(identity = loginDetails["email"])
                return {"access_token" : access_token}, 200

    return {"error" : "Invalid login details provided!"}, 401

def getUserName(userID):
    user = User.query.filter_by(userID=userID).first()
    if user:
        return {"firstName" : current_user.firstName, "lastName": current_user.lastName}
    
    return json.dumps({"error" : "User not found!"})

def identifyUser(current_user):
    if current_user:
        return {"email" : current_user.email, "firstName" : current_user.firstName, "lastName": current_user.lastName}, 200
    
    return json.dumps({"error" : "User is not logged in!"}), 401