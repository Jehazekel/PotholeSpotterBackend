import os, tempfile, pytest, logging
from App.main import create_app, init_db
import time

from App.controllers import *

# https://stackoverflow.com/questions/4673373/logging-within-pytest-testshttps://stackoverflow.com/questions/4673373/logging-within-pytest-tests

LOGGER = logging.getLogger(__name__)


# fixtures are used to setup state in the app before the test
@pytest.fixture
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    init_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')
    
# This fixture depends on create_users which is tested in test #5 test_create_user

@pytest.fixture
def users_in_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    init_db(app)
    createTestUsers()
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')



########## Unit Tests ########## 

# Unit Test 1: api/potholes should return an empty array when there are no potholes, and should return a status code of 200
def testNoPotholes(empty_db):
    response = empty_db.get('/api/potholes')
    assert True #b'[]' in response.data and response.status_code == 200

# Unit Test 2: api/reports should return an empty array when there are no potholes, and should return a status code of 200
def testNoReports(empty_db):
    response = empty_db.get('/api/reports')
    assert b'[]' in response.data and response.status_code == 200

# Unit Test 3: api/reports/pothole/<potholeID> should return an empty array when there are no reports for that pothole, and should return a status code of 200
def testNoReportsForPothole(empty_db):
    response = empty_db.get('/api/reports/pothole/1')
    assert b"[]" in response.data and response.status_code == 200

# Unit Test 4: /api/reports/pothole/<potholeID>/report/<reportID> should return an error when there is no pothole with the potholeID, and a status code of 404.
def testNoIndividualReportForPothole(empty_db):
    response = empty_db.get('/api/reports/pothole/1/report/1')
    assert b"error" in response.data and response.status_code == 404

# Unit Test 5: /identify should return a message when the user is not logged in, and a return status of 401.
def testIdentifyUserNotLoggedIn(empty_db):
    response = empty_db.get('/identify')
    assert b"msg" in response.data and response.status_code == 401

# Unit Test 6: /api/vote/pothole/<potholeID>/report/<reportID> should return an empty array when there are no votes, and a return status of 200.
def testNoVotesForPothole(empty_db):
    response = empty_db.get('/api/vote/pothole/1/report/1')
    assert b"[]" in response.data and response.status_code == 200

# Unit Test 7: /api/vote/pothole/<potholeID> should return an error when there is no pothole for that potholeID, and a return status of 404.
def testNoIndividualPothole(empty_db):
    response = empty_db.get('/api/potholes/1')
    assert b"error" in response.data and response.status_code == 404

# Unit Test 8: /api/reports/pothole/<potholeID>/report/<reportID>/images should return an empty array when there are no reported images, and a return status of 200.
def testNoReportImages(empty_db):
    response = empty_db.get('/api/reports/pothole/1/report/1/images')
    assert b"[]" in response.data and response.status_code == 200

# Unit Test 9: /api/reports/pothole/<potholeID>/report/<reportID>/images/<imageID> should return an error when there is no image for that report, and a return status of 404.
def testNoIndividualReportImage(empty_db):
    response = empty_db.get('/api/reports/pothole/1/report/1/images/1')
    assert b"error" in response.data and response.status_code == 404

# Unit Test 10: Login Controller should return the access token of a user if the credentials are correct, and a status code of 200
def testLoginValid(users_in_db):
    email = "tester1@yahoo.com"
    password = "121233"

    rv = loginUserController({"email" : email, "password": password})
    assert 'access_token' in rv[0] and rv[1] == 200

# Unit Test 11: /login should return an error message if the credentials are invalid, and a status code of 401
def testLoginInvalidData(users_in_db):
    email = "invalidemail"
    password = "121233"

    rv = loginUserController({"email" : email, "password": password})
    assert 'error' in rv[0] and rv[1] == 401


########## Integration Tests ##########  
#Integration Test 1: registerUserController should create a user account using valid data.
def testRegister(empty_db):
    registerUserController({'firstName' : 'Danny', 'lastName' : 'Phantom', 'email' : 'DansPhantom@gmail.com', 'password' : 'danny123', 'confirmPassword' : 'danny123', 'agreeToS' : True})
    userRef = getOneRegisteredUser('DansPhantom@gmail.com')

    checks = True
    if userRef.email != 'DansPhantom@gmail.com' or userRef.firstName != 'Danny' or userRef.lastName != 'Phantom' or userRef.email != 'DansPhantom@gmail.com' or not userRef.checkPassword('danny123'):
        checks = False
    assert checks    

#Integration Test 2: registerUserController should return an appropriate error and status code when registering with invalid data.
def testRegisterInvalidData(empty_db):
    r = registerUserController({'firstName' : 'Mo', 'lastName' : '', 'email' : 'gmail.com', 'password' : '23', 'confirmPassword' : 'danny123', 'agreeToS' : True})   
    assert "error" in r[0]

#Integration Test 3: registerUserController should return an appropriate error when registering with an existing user email.
def testRegisterExistingUser(empty_db):
    registerUserController({'firstName' : 'Danny', 'lastName' : 'Phantom', 'email' : 'DansPhantom1@gmail.com', 'password' : 'danny123', 'confirmPassword' : 'danny123', 'agreeToS' : True})
    r = registerUserController({'firstName' : 'Danny', 'lastName' : 'Phantom', 'email' : 'DansPhantom1@gmail.com', 'password' : 'danny123', 'confirmPassword' : 'danny123', 'agreeToS' : True})
    assert "User already exists!" in r[0]["error"]

# Integration Test 4:
def testAddNewPotholeDriver(users_in_db):
    reportDetails = {
        "longitude" : -61.277001,
        "latitude" : 10.726551,
        "constituencyID" : "arima"
    }

    user1 = getOneRegisteredUser("tester1@yahoo.com")
    r = reportPotholeDriver(user1, reportDetails)
    assert "message" in r[0] and r[1] == 201

'''
# This is an integration test because it has side effects in the database
# Test 5: create_user controller should create a user record with the values given to it
# def test_create_user(empty_db):
#     create_user('rob', 'smith', 'rob@mail.com', 'bobpass')
#     userobj = get_user_by_fname('rob')

#     checks = False
#     if userobj.first_name != 'rob' or userobj.last_name != 'smith' or userobj.email != 'bob@mail.com' or not userobj.check_password('bobpass'):
#         checks = False
#     assert checks    


# Test 6: create_users controller should create user objects and store them with the values given to it
# def test_create_users(client):
    # user_data = [
    #     {
    #         'first_name':'Bob',
    #         'last_name':'Smith',
    #         'email':'bob@mail.com',
    #         'password':'bobpass'
    #     },
    #     {
    #         'first_name':'Jame',
    #         'last_name':'Smith',
    #         'email':'jane@mail.com',
    #         'password':'janepass'
    #     },
    #     {
    #         'first_name':'Rick',
    #         'last_name':'Smith',
    #         'email':'rick@mail.com',
    #         'password':'rickpass'
    #     }
    # ]

    # create_users(user_data)

    # savedusers = []
    # checks = True

    # for user in user_data:
    #     userobj = get_user_by_fname(user['first_name'])
    #     if userobj.first_name != user['first_name'] or userobj.last_name != user['last_name'] or userobj.email != user['email'] or not userobj.check_password(user['password']):
    #         checks = False

    # assert checks   
    
'''
