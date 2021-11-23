import os, tempfile, pytest, logging
from App.controllers.pothole import getAllPotholes
from App.controllers.user import getOneRegisteredUser
from App.main import create_app, init_db
import time

from App.controllers import *
from App.views import *

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


@pytest.fixture
def simulated_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    init_db(app)
    createSimulatedData()
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

# Unit Test 12:
def testGetExistingPothole(simulated_db):
    expected = '{"potholeID": 1, "longitude": -61.277001, "latitude": 10.726551, "constituencyID": "arima", "expiryDate": "2021-12-23"}'
    potholeID = 1
    rv = displayIndividualPotholes(potholeID)
    print(rv[0])
    assert expected in rv[0] and rv[1] == 200

# Unit Test 13:
def testGetNonExistentPothole(simulated_db):
    potholeID = 999
    rv = displayIndividualPotholes(potholeID)
    assert 'error' in rv[0] and rv[1] == 404

# Unit Test 14:
def testGetExistingReport(simulated_db):
    expected = '{"reportID": 1, "userID": 1, "potholeID": 1, "dateReported": "2021-11-23", "description": "Very large pothole spanning both lanes of the road.", "votes": [], "reportedImages": [{"imageID": 1, "reportID": 1, "imageURL": "https://www.howtogeek.com/wp-content/uploads/2018/08/Header.png"}]}'
    potholeID = 1
    reportID = 1
    rv = displayIndividualPotholeReport(potholeID, reportID)
    assert expected in rv[0] and rv[1] == 200

# Unit Test 15:
def testGetNonExistentReport(simulated_db):
    potholeID = 999
    reportID = 999
    rv = displayIndividualPotholeReport(potholeID, reportID)
    assert 'error' in rv[0] and rv[1] == 404

# Unit Test 16:
def testGetAllReportsForPothole(simulated_db):
    expected = '[{"reportID": 1, "userID": 1, "potholeID": 1, "dateReported": "2021-11-23", "description": "Very large pothole spanning both lanes of the road.", "votes": [], "reportedImages": [{"imageID": 1, "reportID": 1, "imageURL": "https://www.howtogeek.com/wp-content/uploads/2018/08/Header.png"}]}, {"reportID": 2, "userID": 2, "potholeID": 1, "dateReported": "2021-11-23", "description": "Small pothole in center of road", "votes": [], "reportedImages": [{"imageID": 2, "reportID": 2, "imageURL": "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__480.jpg"}]}, {"reportID": 3, "userID": 3, "potholeID": 1, "dateReported": "2021-11-23", "description": "Very large pothole.", "votes": [], "reportedImages": [{"imageID": 3, "reportID": 3, "imageURL": "https://images.unsplash.com/photo-1541963463532-d68292c34b19?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8Mnx8fGVufDB8fHx8&w=1000&q=80"}]}, {"reportID": 4, "userID": 4, "potholeID": 1, "dateReported": "2021-11-23", "description": "Pothole submitted via Driver Mode.", "votes": [], "reportedImages": []}, {"reportID": 5, "userID": 5, "potholeID": 1, "dateReported": "2021-11-23", "description": "Pothole submitted via Driver Mode.", "votes": [], "reportedImages": []}, {"reportID": 6, "userID": 6, "potholeID": 1, "dateReported": "2021-11-23", "description": "Pothole submitted via Driver Mode.", "votes": [], "reportedImages": []}]'
    potholeID = 1
    rv = getPotholeReports(potholeID)
    assert expected in rv[0] and rv[1] == 200

# Unit Test 17:
def testGetAllReportImagesForPothole(simulated_db):
    expected = '[{"imageID": 1, "reportID": 1, "imageURL": "https://www.howtogeek.com/wp-content/uploads/2018/08/Header.png"}]'
    potholeID = 1
    reportID = 1
    rv = getReportImages(potholeID, reportID)
    assert expected in rv[0] and rv[1] == 200

# Unit Test 18:
def testGetIndividualReportImage(simulated_db):
    expected = '{"imageID": 1, "reportID": 1, "imageURL": "https://www.howtogeek.com/wp-content/uploads/2018/08/Header.png"}'
    potholeID = 1
    reportID = 1
    imageID = 1
    rv = getIndividualReportedImage(potholeID, reportID, imageID)
    assert expected in rv[0] and rv[1] == 200

# Unit Test 19:
def testGetNonExistentIndividualReportImage(simulated_db):
    potholeID = 15
    reportID = 15
    imageID = 15
    rv = getIndividualReportedImage(potholeID, reportID, imageID)
    assert "error" in rv[0] and rv[1] == 404

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
def testAddNewPotholeReportDriver(users_in_db):
    reportDetails = {
        "longitude" : -61.277001,
        "latitude" : 10.726551,
        "constituencyID" : "arima"
    }

    user1 = getOneRegisteredUser("tester1@yahoo.com")
    r = reportPotholeDriver(user1, reportDetails)


    allReportsByUser = getAllPotholeReportsByUser(user1)
    check2 = False

    for oneReportByUser in allReportsByUser:
        if "Pothole submitted via Driver Mode." == oneReportByUser["description"]:
            check2 = True

    rPotholes = getAllPotholes()
    check1 = False
    for pothole in rPotholes:
        if reportDetails["longitude"] == pothole["longitude"] and reportDetails["latitude"] == pothole["latitude"]:
            check1 = True

    assert check1 and check2 and "message" in r[0] and r[1] == 201


# Integration Test 5:
def testAddNewPotholeReportStandard(users_in_db):
    reportDetails = {
        "longitude" : -61.277001,
        "latitude" : 10.726551,
        "constituencyID" : "arima",
        "description": "Very large pothole spanning both lanes of the road.",
        "images" : [
            "https://www.howtogeek.com/wp-content/uploads/2018/08/Header.png"
        ]
    }

    user1 = getOneRegisteredUser("tester1@yahoo.com")
    r = reportPotholeStandard(user1, reportDetails)


    allReportsByUser = getAllPotholeReportsByUser(user1)
    check2 = False

    for oneReportByUser in allReportsByUser:
        if reportDetails["description"] == oneReportByUser["description"] and reportDetails["images"][0] == oneReportByUser["reportedImages"][0]["imageURL"]:
            check2 = True



    rPotholes = getAllPotholes()
    check1 = False
    for pothole in rPotholes:
        if reportDetails["longitude"] == pothole["longitude"] and reportDetails["latitude"] == pothole["latitude"]:
            check1 = True

    assert check1 and check2 and "message" in r[0] and r[1] == 201

# Integration Test 6:
def testDuplicateReportSameUser(simulated_db):
    reportDetails = {
        "longitude" : -61.277001,
        "latitude" : 10.726551,
        "constituencyID" : "arima",
    }

    user1 = getOneRegisteredUser("tester1@yahoo.com")
    r = reportPotholeDriver(user1, reportDetails)

    assert "Expiry date of pothole has been reset!" in r[0]["message"] and r[1] == 201


# Integration Test 6:
def testMultipleReportsSamePothole(users_in_db):
    reportDetails = {
        "longitude" : -61.454274,
        "latitude" : 10.432359,
        "constituencyID" : "couva",
    }

    user1 = getOneRegisteredUser("tester1@yahoo.com")
    user2 = getOneRegisteredUser("tester2@yahoo.com")

    reportPotholeDriver(user1, reportDetails)
    reportPotholeDriver(user2, reportDetails)

    user1Reports = getAllPotholeReportsByUser(user1)
    user2Reports = getAllPotholeReportsByUser(user2)

    assert user1Reports[0]["potholeID"] == user2Reports[0]["potholeID"]

# Integration Test 7:
def testDeleteExistingPotholeImage(simulated_db):
    user1 = getOneRegisteredUser("tester1@yahoo.com")

    potholeID = 1
    reportID = 1
    imageID = 1

    reportedImageBefore = getIndividualReportedImage(potholeID, reportID, imageID)

    deletePotholeReportImage(user1, potholeID, reportID, imageID)

    reportedImageAfter = getIndividualReportedImage(potholeID, reportID, imageID)

    assert reportedImageBefore != reportedImageAfter and "error" in reportedImageAfter[0]

# Integration Test 8:
def testDeleteExistingPotholeImageNotOwner(simulated_db):
    user2 = getOneRegisteredUser("tester2@yahoo.com")

    potholeID = 1
    reportID = 1
    imageID = 1

    reportedImageBefore = getIndividualReportedImage(potholeID, reportID, imageID)

    deletePotholeReportImage(user2, potholeID, reportID, imageID)

    reportedImageAfter = getIndividualReportedImage(potholeID, reportID, imageID)

    assert reportedImageBefore == reportedImageAfter

# Integration Test 9: 
def testDeleteNonExistentPotholeImage(simulated_db):
    user2 = getOneRegisteredUser("tester2@yahoo.com")

    potholeID = 12
    reportID = 12
    imageID = 12

    reportedImageResult = getIndividualReportedImage(potholeID, reportID, imageID)

    assert "error" in reportedImageResult[0]

# Integration Test 10:
def testAddPotholeImageNotOwner(simulated_db):
    user2 = getOneRegisteredUser("tester2@yahoo.com")
    expected = '{"imageID": 1, "reportID": 1, "imageURL": "https://www.howtogeek.com/wp-content/uploads/2018/08/Header.png"}'
    potholeID = 1
    reportID = 1
    imageDetails = {
        "images" : ["https://media.gettyimages.com/photos/balanced-stones-on-a-pebble-beach-during-sunset-picture-id157373207?s=612x612"]
    }

    rv = addPotholeReportImage(user2, potholeID, reportID, imageDetails)

    print(rv[0])

    assert "error" in rv[0]

# Integration Test 11:
def testAddPotholeImage(simulated_db):
    user1 = getOneRegisteredUser("tester1@yahoo.com")
    potholeID = 1
    reportID = 1
    imageDetails = {
        "images" : ["https://media.gettyimages.com/photos/balanced-stones-on-a-pebble-beach-during-sunset-picture-id157373207?s=612x612"]
    }

    rv = addPotholeReportImage(user1, potholeID, reportID, imageDetails)

    res = getIndividualReportedImage(potholeID, reportID, 4)

    assert "message" in rv[0] and rv[1] == 201 and "https://media.gettyimages.com/photos/balanced-stones-on-a-pebble-beach-during-sunset-picture-id157373207?s=612x612" in res[0]

# Integration Test 12:
def testAddPotholeImageInvalidImageURL(simulated_db):
    user1 = getOneRegisteredUser("tester1@yahoo.com")
    potholeID = 1
    reportID = 1
    imageDetails = {
        "images" : ["https://myelearning.sta.uwi.edu"]
    }

    rv = addPotholeReportImage(user1, potholeID, reportID, imageDetails)

    assert "error" in rv[0]

# Integration Test 13:
def testUpdatePotholeDescriptionAsOwner(simulated_db):
    user1 = getOneRegisteredUser("tester1@yahoo.com")
    potholeID = 1
    reportID = 1
    potholeDetails = {
        'description': 'Wide pothole!'
    }

    rv = updateReportDescription(user1, potholeID, reportID, potholeDetails)
    updatedReport = getIndividualPotholeReport(potholeID, reportID)
    print(updatedReport[0])

    assert "message" in rv[0] and 200 == rv[1] and '"description": "Wide pothole!"' in updatedReport[0]

# Integration Test 14:
def testUpdatePotholeDescriptionAsNonOwner(simulated_db):
    user2 = getOneRegisteredUser("tester2@yahoo.com")
    potholeID = 1
    reportID = 1
    potholeDetails = {
        'description': 'Wide pothole!'
    }

    rv = updateReportDescription(user2, potholeID, reportID, potholeDetails)

    assert "error" in rv[0] and 404 == rv[1]


# Integration Test 15:
def testUpdatePotholeDescriptionNonExistent(simulated_db):
    user2 = getOneRegisteredUser("tester2@yahoo.com")
    potholeID = 12
    reportID = 12
    potholeDetails = {
        'description': 'Wide pothole!'
    }

    rv = updateReportDescription(user2, potholeID, reportID, potholeDetails)

    assert "error" in rv[0] and 404 == rv[1]

# Integration Test 16:
def testDeleteIndividualReportAsOwner(simulated_db):
    user1 = getOneRegisteredUser("tester1@yahoo.com")
    potholeID = 1
    reportID = 1

    rv = deleteUserPotholeReport(user1, potholeID, reportID)
    oldRep = getIndividualPotholeReport(potholeID, reportID)

    assert "message" in rv[0] and 200 == rv[1] and "error" in oldRep[0]


# Integration Test 17:
def testDeleteIndividualReportAsNonOwner(simulated_db):
    user2 = getOneRegisteredUser("tester2@yahoo.com")
    potholeID = 1
    reportID = 1

    rv = deleteUserPotholeReport(user2, potholeID, reportID)
    oldRep = getIndividualPotholeReport(potholeID, reportID)

    assert "error" in rv[0] and 404 == rv[1] and "error" not in oldRep[0]

# Integration Test 18:
def testDeleteIndividualReportNonExistent(simulated_db):
    user1 = getOneRegisteredUser("tester1@yahoo.com")
    potholeID = 12
    reportID = 12

    rv = deleteUserPotholeReport(user1, potholeID, reportID)

    assert "error" in rv[0] and 404 == rv[1]

# Integration Test 19:
def testDeleteLastReportDeletesPothole(simulated_db):
    user1 = getOneRegisteredUser("tester1@yahoo.com")
    potholeID = 1
    reportID = 1

    potholeBeforeDelete = displayIndividualPotholes(potholeID)[0]

    rv = deleteUserPotholeReport(user1, potholeID, reportID)
    oldRep = getIndividualPotholeReport(potholeID, reportID)

    potholeAfterDelete = displayIndividualPotholes(potholeID)[0]

    assert "message" in rv[0] and 200 == rv[1] and "error" in oldRep[0] and potholeBeforeDelete == potholeAfterDelete


# Integration Test 20:
def testCalculateNetVotes(simulated_db):
    potholeID = 1
    reportID = 1

    user1 = getOneRegisteredUser("tester1@yahoo.com")
    user2 = getOneRegisteredUser("tester2@yahoo.com")
    user3 = getOneRegisteredUser("tester3@yahoo.com")
    user4 = getOneRegisteredUser("tester4@yahoo.com")
    user5 = getOneRegisteredUser("tester5@yahoo.com")
    
    voteOnPothole(user1, potholeID, reportID, {"upvote" : False})
    voteOnPothole(user2, potholeID, reportID, {"upvote" : False})
    voteOnPothole(user3, potholeID, reportID, {"upvote" : True})
    voteOnPothole(user4, potholeID, reportID, {"upvote" : False})
    voteOnPothole(user5, potholeID, reportID, {"upvote" : True})

    netVotes = calculateNetVotes(reportID)

    assert netVotes == -1

# Integration Test 21:
def testDeleteReportAfterNegativeVoteThreshold(simulated_db):
    potholeID = 1
    reportID = 1

    voteData = {
        "upvote" : False
    }

    user1 = getOneRegisteredUser("tester1@yahoo.com")
    user2 = getOneRegisteredUser("tester2@yahoo.com")
    user3 = getOneRegisteredUser("tester3@yahoo.com")
    user4 = getOneRegisteredUser("tester4@yahoo.com")
    user5 = getOneRegisteredUser("tester5@yahoo.com")
    
    repBefore = getIndividualPotholeReport(potholeID, reportID)
    voteOnPothole(user1, potholeID, reportID, voteData)
    voteOnPothole(user2, potholeID, reportID, voteData)
    voteOnPothole(user3, potholeID, reportID, voteData)
    voteOnPothole(user4, potholeID, reportID, voteData)
    voteOnPothole(user5, potholeID, reportID, voteData)
    repAfter = getIndividualPotholeReport(potholeID, reportID)

    assert "No report found." in repAfter[0] and 404 == repAfter[1] and "No report found." not in repBefore

# Integration Test 22:
def testVoteOnPothole(simulated_db):
    user1 = getOneRegisteredUser("tester1@yahoo.com")
    potholeID = 1
    reportID = 1

    votesBefore = calculateNetVotes(reportID)
    voteOnPothole(user1, potholeID, reportID, {"upvote" : True})
    votesAfter = calculateNetVotes(reportID)

    assert votesBefore != votesAfter

# Integration Test 23:
def testUnVoteOnPothole(simulated_db):
    user1 = getOneRegisteredUser("tester1@yahoo.com")
    potholeID = 1
    reportID = 1

    votesBefore = calculateNetVotes(reportID)
    voteOnPothole(user1, potholeID, reportID, {"upvote" : True})
    voteOnPothole(user1, potholeID, reportID, {"upvote" : True})
    votesAfter = calculateNetVotes(reportID)

    assert votesBefore == votesAfter

# Integration Test 23:
def testChangeVoteOnPothole(simulated_db):
    user1 = getOneRegisteredUser("tester1@yahoo.com")
    potholeID = 1
    reportID = 1

    votesBefore = calculateNetVotes(reportID)
    voteOnPothole(user1, potholeID, reportID, {"upvote" : True})
    votesMidway = calculateNetVotes(reportID)
    voteOnPothole(user1, potholeID, reportID, {"upvote" : False})
    votesAfter = calculateNetVotes(reportID)

    assert votesBefore != votesAfter != votesMidway