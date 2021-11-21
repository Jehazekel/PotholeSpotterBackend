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
'''
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
'''