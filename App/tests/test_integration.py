import os, tempfile, pytest, logging
from App.main import create_app, init_db
import time

from App.controllers import *

# https://stackoverflow.com/questions/4673373/logging-within-pytest-testshttps://stackoverflow.com/questions/4673373/logging-within-pytest-tests

LOGGER = logging.getLogger(__name__)

# fixtures are used to setup state in the app before the test
# This fixture creates an empty database for the test and deletes it after the test
def deleteDBFile(dir):
    os.close(os.getcwd()+dir)
    os.unlink(os.getcwd()+dir)


@pytest.fixture
def empty_db():
    deleteDBFile('/App/test.db')
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    init_db(app)
    yield app.test_client()
    deleteDBFile('/App/test.db')
    
# This fixture depends on create_users which is tested in test #5 test_create_user

@pytest.fixture
def users_in_db():
    deleteDBFile('/App/test.db')
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    init_db(app)
    createTestUsers()
    yield app.test_client()
    deleteDBFile('/App/test2.db')

########## Integration Tests ##########  
'''
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
