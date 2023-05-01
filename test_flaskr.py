import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dateutil.parser import parse

from flaskr import create_app
from models import setup_db, Hall, Couple

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'event_management_test')
DB_PATH = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)



import json
import requests

# testing user password database:
testingUsers = {
    'kavia_testing@testmail.com': 'Password1234',
    'kavia_testing_officer@testmail.com': 'Password*Officer',
    'kavia_testing_customer@testmail.com': 'Password*Customer',
    'kavia_testing_decorator@testmail.com': 'Password*Decorator'
    }


def getUserToken(userName):
    # client id and secret come from LogIn (Test Client)! which has password enabled under "Client > Advanced > Grant Types > Tick Password"
    url = 'https://udacity-fullstack-kavia-auth.us.auth0.com/oauth/token' 
    headers = {'content-type': 'application/json'}
    password = testingUsers[userName]
    parameter = { "client_id":"57b0nWhidtmko1oZidS3mDNiBXoG70aH", 
                  "audience": 'wedding',
                  "grant_type": "password",
                  "username": userName,
                  "password": password, "scope": "openid" } 
    # do the equivalent of a CURL request from https://auth0.com/docs/quickstart/backend/python/02-using#obtaining-an-access-token-for-testing
    responseDICT = json.loads(requests.post(url, json=parameter, headers=headers).text)
    #print(responseDICT)
    return responseDICT['access_token']


#@memoize # memoize code from: https://stackoverflow.com/a/815160
def getUserTokenHeaders(userName='kavia_testing@testmail.com'):
    return { 'Authorization' : "Bearer " + getUserToken(userName)} 


header = getUserTokenHeaders()
officer_header = getUserTokenHeaders('kavia_testing_officer@testmail.com')
decorator_header = getUserTokenHeaders('kavia_testing_decorator@testmail.com')
customer_header = getUserTokenHeaders('kavia_testing_customer@testmail.com')

class EventManagementTestCase(unittest.TestCase):
    """This class represents the Event Management test case"""
    @classmethod
    def setUpClass(self):
        self.app = create_app(test_config={
            "SQLALCHEMY_DATABASE_URI": DB_PATH
        })

    def setUp(self):
        """Defining test variables and initializing app."""  
        self.app = create_app(reset_db=False, test_config={
            "SQLALCHEMY_DATABASE_URI": DB_PATH
        })
        self.client = self.app.test_client
#        setup_db(self.app)

        self.new_couple = {
            "bride_name" : "new_bride_officer",
            "groom_name" : "new_groom_officer",
            "marriage_date" : "2023-07-28 5:00:55",
            "email_id" : "new_officer@gmail.com",
            "hall" : 2
        }

        self.new_couple_with_date_misformat = {
            "bride_name" : "new_bride",
            "groom_name" : "new_groom",
            "marriage_date" : "2023-02-29 5:00:55",
            "email_id" : "new@gmail.com",
            "hall" : 2
        }

        self.new_couple_with_invalid_hall = {
            "bride_name" : "new_bride",
            "groom_name" : "new_groom",
            "marriage_date" : "2023-06-28 5:00:55",
            "email_id" : "new@gmail.com",
            "hall" : 200
        } 

        self.update_couple = {
            "marriage_date" : "2023-06-28 4:00:00",
            "email_id" : "updated_email@gmail.com",
            "wedding_theme" : "Grand Tamil Traditional",
            "hall" : 2
        }

        self.update_couple_as_officer = {
            "marriage_date" : "2023-07-28 4:00:00",
            "email_id" : "updated_email_as_officer@gmail.com",
            "wedding_theme" : "Tamil Thirumanam"
        }

        self.update_couple_with_date_misformat = {
            "marriage_date" : "2023-20-28 4:00:00",
            "email_id" : "updated_email@gmail.com",
            "wedding_theme" : "Grand Tamil Traditional",
            "hall" : 2
        }
    
        self.update_couple_with_invalid_hall = {
            "marriage_date" : "2023-06-28 4:00:00",
            "email_id" : "updated_email@gmail.com",
            "wedding_theme" : "Grand Tamil Traditional",
            "hall" : 300
        }

        self.new_hall = {
            'name': 'Mahindra',
            'capacity': 500,
            'price': 30000,
            'address': 'Tamil Nadu, Chennai'            
        }
        
        self.new_hall_with_price_missing = {
            'name': 'Mahindra',
            'price': 30000,
            'address': 'Tamil Nadu, Chennai'            
        }

        self.update_hall = {
            'capacity': 100,
            'price': 100000
        }

        self.update_hall_with_invalid_price = {
            'capacity': 100,
            'price': '₹ 100000'
        }
        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass
    
    def test_get_couples(self):
        res = self.client().get("/couples", headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["couples"]))
        self.assertTrue(data["total_couples"])
        self.assertEqual(len(data["couples"]), data["total_couples"])

    def test_get_couple_by_id(self):
        res = self.client().get("/couples/2", headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["couple"])
        self.assertEqual(data["couple"].get("id"), 2)

    def test_404_for_invalid_couple_id(self):
        res = self.client().get("/couples/1000", headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    
    def test_create_new_couple(self):
        res = self.client().post("/couples", json=self.new_couple, headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

        couple = Couple.query.filter(Couple.id == data["created"].get("id")).one_or_none()
        self.assertTrue(couple)
        
    
    def test_405_if_couple_creation_not_allowed(self):
        res = self.client().post("/couples/3", json=self.new_couple, headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    
    def test_400_if_date_misformat_in_create_couple(self):
        res = self.client().post("/couples", json=self.new_couple_with_date_misformat, headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request - Error in parsing Marriage date : day is out of range for month")

    def test_422_if_foreign_key_violation_in_create_couple(self):
        res = self.client().post("/couples", json=self.new_couple_with_invalid_hall, headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_update_couple(self):
        res = self.client().patch("/couples/2", json=self.update_couple, headers = header)
        data = json.loads(res.data)
        
        couple = Couple.query.filter(Couple.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["updated"])

        self.assertEqual(data["updated"].get("id"), 2)
        self.assertEqual(data["updated"].get("marriage_date"), "Wed, 28 Jun 2023 04:00:00 GMT")
        self.assertEqual(data["updated"].get("wedding_theme"), "Grand Tamil Traditional")
        self.assertEqual(data["updated"].get("hall"), 2)

        self.assertEqual(couple.format().get("marriage_date"), parse("2023-06-28 4:00:00"))
        self.assertEqual(couple.format().get("wedding_theme"), "Grand Tamil Traditional")
        self.assertEqual(couple.format().get("hall"), 2)
    
    def test_404_update_with_invalid_couple_id(self):
        res = self.client().patch("/couples/10000", json=self.update_couple, headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_400_if_date_misformat_in_update_couple(self):
        res = self.client().patch("/couples/2", json=self.update_couple_with_date_misformat, headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request - Error in parsing Marriage date : month must be in 1..12")
    
    def test_422_if_foreign_key_violation_in_update_couple(self):
        res = self.client().patch("/couples/2", json=self.update_couple_with_invalid_hall, headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_delete_couple(self):
        res = self.client().delete('/couples/1', headers = header)
        data = json.loads(res.data)

        couple = Couple.query.filter(Couple.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(data['total_couples'])
        self.assertTrue(len(data['couples']))
        self.assertEqual(data['total_couples'], len(data['couples']))
        self.assertFalse(couple)

    def test_404_if_couple_does_not_exist_while_deleting(self):
        res = self.client().delete("/couples/1000", headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


    def test_get_halls(self):
        res = self.client().get("/halls", headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["halls"]))
        self.assertTrue(data["total_halls"])
        self.assertEqual(len(data["halls"]), data["total_halls"])

    def test_get_hall_by_id(self):
        res = self.client().get("/halls/2", headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["hall"])
        self.assertEqual(data["hall"].get("id"), 2)

    def test_404_for_invalid_hall_id(self):
        res = self.client().get("/halls/1000", headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    
    def test_create_new_hall(self):
        res = self.client().post("/halls", json=self.new_hall, headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

        hall = Hall.query.filter(Hall.id == data["created"].get("id")).one_or_none()
        self.assertTrue(hall)
        
    def test_405_if_hall_creation_not_allowed(self):
        res = self.client().post("/halls/3", json=self.new_hall, headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    
    def test_422_if_field_missing_in_create_hall(self):
        res = self.client().post("/halls", json=self.new_hall_with_price_missing, headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_update_hall(self):
        res = self.client().patch("/halls/2", json=self.update_hall, headers = header)
        data = json.loads(res.data)
        
        hall = Hall.query.filter(Hall.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["updated"])

        self.assertEqual(data["updated"].get("id"), 2)
        self.assertEqual(data["updated"].get("capacity (number of persons)"), 100)
        self.assertEqual(float(data["updated"].get("price (per day)")), 100000.00)

        self.assertEqual(hall.format().get("capacity (number of persons)"), 100)
        self.assertEqual(float(hall.format().get("price (per day)")), 100000.00)
    
    def test_404_update_with_invalid_hall_id(self):
        res = self.client().patch("/halls/20000", json=self.update_hall, headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_422_if_datetype_mismatch_in_update_hall(self):
        res = self.client().patch("/halls/2", json=self.update_hall_with_invalid_price, headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    def test_delete_hall(self):
        res = self.client().delete('/halls/1', headers = header)
        data = json.loads(res.data)

        hall = Hall.query.filter(Hall.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(data['total_halls'])
        self.assertTrue(len(data['halls']))
        self.assertEqual(data['total_halls'], len(data['halls']))
        self.assertFalse(hall)

    def test_404_if_hall_does_not_exist_while_deleting(self):
        res = self.client().delete("/halls/30000", headers = header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")





    def test_get_couples_as_officer(self):
        res = self.client().get("/couples", headers = officer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["couples"]))
        self.assertTrue(data["total_couples"])
        self.assertEqual(len(data["couples"]), data["total_couples"])

    def test_get_couple_by_id_as_officer(self):
        res = self.client().get("/couples/2", headers = officer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["couple"])
        self.assertEqual(data["couple"].get("id"), 2)

    def test_404_for_invalid_couple_id_as_officer(self):
        res = self.client().get("/couples/1000", headers = officer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    
    def test_create_new_couple_as_officer(self):
        res = self.client().post("/couples", json=self.new_couple, headers = officer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

        couple = Couple.query.filter(Couple.id == data["created"].get("id")).one_or_none()
        self.assertTrue(couple)
    
    def test_405_if_couple_creation_not_allowed_as_officer(self):
        res = self.client().post("/couples/3", json=self.new_couple, headers = officer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    
    def test_400_if_date_misformat_in_create_couple_as_officer(self):
        res = self.client().post("/couples", json=self.new_couple_with_date_misformat, headers = officer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request - Error in parsing Marriage date : day is out of range for month")

    def test_422_if_foreign_key_violation_in_create_couple_as_officer(self):
        res = self.client().post("/couples", json=self.new_couple_with_invalid_hall, headers = officer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_update_couple_as_officer(self):
        res = self.client().patch("/couples/2", json=self.update_couple_as_officer, headers = officer_header)
        data = json.loads(res.data)
        
        couple = Couple.query.filter(Couple.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["updated"])

        self.assertEqual(data["updated"].get("id"), 2)
        self.assertEqual(data["updated"].get("marriage_date"), "Fri, 28 Jul 2023 04:00:00 GMT")
        self.assertEqual(data["updated"].get("wedding_theme"), "Tamil Thirumanam")
        self.assertEqual(data["updated"].get("email_id"), "updated_email_as_officer@gmail.com")

        self.assertEqual(couple.format().get("marriage_date"), parse("2023-07-28 4:00:00"))
        self.assertEqual(couple.format().get("wedding_theme"), "Tamil Thirumanam")
        self.assertEqual(couple.format().get("email_id"), "updated_email_as_officer@gmail.com")
    
    def test_404_update_with_invalid_couple_id_as_officer(self):
        res = self.client().patch("/couples/10000", json=self.update_couple, headers = officer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_400_if_date_misformat_in_update_couple_as_officer(self):
        res = self.client().patch("/couples/2", json=self.update_couple_with_date_misformat, headers = officer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request - Error in parsing Marriage date : month must be in 1..12")
    
    def test_422_if_foreign_key_violation_in_update_couple_as_officer(self):
        res = self.client().patch("/couples/2", json=self.update_couple_with_invalid_hall, headers = officer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_delete_couple_as_officer(self):
        res = self.client().delete('/couples/3', headers = officer_header)
        data = json.loads(res.data)

        couple = Couple.query.filter(Couple.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 3)
        self.assertTrue(data['total_couples'])
        self.assertTrue(len(data['couples']))
        self.assertEqual(data['total_couples'], len(data['couples']))
        self.assertFalse(couple)

    def test_404_if_couple_does_not_exist_while_deleting_as_officer(self):
        res = self.client().delete("/couples/1000", headers = officer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


    def test_get_halls_as_officer(self):
        res = self.client().get("/halls", headers = officer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["halls"]))
        self.assertTrue(data["total_halls"])
        self.assertEqual(len(data["halls"]), data["total_halls"])

    def test_get_hall_by_id_as_officer(self):
        res = self.client().get("/halls/2", headers = officer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["hall"])
        self.assertEqual(data["hall"].get("id"), 2)

    def test_create_new_hall_as_officer(self):
        res = self.client().post("/halls", json=self.new_hall, headers = officer_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_update_hall_as_officer(self):
        res = self.client().patch("/halls/2", json=self.update_hall, headers = officer_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')
    
    def test_delete_hall_as_officer(self):
        res = self.client().delete('/halls/1', headers = officer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')




    def test_get_couples_as_decorator(self):
        res = self.client().get("/couples", headers = decorator_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_get_couple_by_id_as_decorator(self):
        res = self.client().get("/couples/2", headers = decorator_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_create_new_couple_as_decorator(self):
        res = self.client().post("/couples", json=self.new_couple, headers = decorator_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

        couple = Couple.query.filter(Couple.id == data["created"].get("id")).one_or_none()
        self.assertTrue(couple)
    
    def test_405_if_couple_creation_not_allowed_as_decorator(self):
        res = self.client().post("/couples/3", json=self.new_couple, headers = decorator_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    
    def test_400_if_date_misformat_in_create_couple_as_decorator(self):
        res = self.client().post("/couples", json=self.new_couple_with_date_misformat, headers = decorator_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request - Error in parsing Marriage date : day is out of range for month")

    def test_422_if_foreign_key_violation_in_create_couple_as_decorator(self):
        res = self.client().post("/couples", json=self.new_couple_with_invalid_hall, headers = decorator_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    def test_update_couple_as_decorator(self):
        res = self.client().patch("/couples/2", json=self.update_couple, headers = decorator_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')    

    def test_delete_couple_as_decorator(self):
        res = self.client().delete('/couples/3', headers = decorator_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_get_halls_as_decorator(self):
        res = self.client().get("/halls", headers = decorator_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["halls"]))
        self.assertTrue(data["total_halls"])
        self.assertEqual(len(data["halls"]), data["total_halls"])

    def test_get_hall_by_id_as_decorator(self):
        res = self.client().get("/halls/2", headers = decorator_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["hall"])
        self.assertEqual(data["hall"].get("id"), 2)

    def test_404_for_invalid_hall_id_as_decorator(self):
        res = self.client().get("/halls/1000", headers = decorator_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_create_new_hall_as_decorator(self):
        res = self.client().post("/halls", json=self.new_hall, headers = decorator_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_update_hall_as_decorator(self):
        res = self.client().patch("/halls/2", json=self.update_hall, headers = decorator_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')
    
    def test_delete_hall_as_decorator(self):
        res = self.client().delete('/halls/1', headers = decorator_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')




    def test_get_couples_as_customer(self):
        res = self.client().get("/couples", headers = customer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_get_couple_by_id_as_customer(self):
        res = self.client().get("/couples/2", headers = customer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_404_for_invalid_couple_id_as_customer(self):
        res = self.client().get("/couples/1000", headers = customer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')
    
    def test_create_new_couple_as_customer(self):
        res = self.client().post("/couples", json=self.new_couple, headers = customer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

        couple = Couple.query.filter(Couple.id == data["created"].get("id")).one_or_none()
        self.assertTrue(couple)
    
    def test_405_if_couple_creation_not_allowed_as_customer(self):
        res = self.client().post("/couples/3", json=self.new_couple, headers = customer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    
    def test_400_if_date_misformat_in_create_couple_as_customer(self):
        res = self.client().post("/couples", json=self.new_couple_with_date_misformat, headers = customer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request - Error in parsing Marriage date : day is out of range for month")

    def test_422_if_foreign_key_violation_in_create_couple_as_customer(self):
        res = self.client().post("/couples", json=self.new_couple_with_invalid_hall, headers = customer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_update_couple_as_customer(self):
        res = self.client().patch("/couples/2", json=self.update_couple, headers = customer_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')    

    def test_delete_couple_as_customer(self):
        res = self.client().delete('/couples/3', headers = customer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_get_halls_as_customer(self):
        res = self.client().get("/halls", headers = customer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_get_hall_by_id_as_customer(self):
        res = self.client().get("/halls/2", headers = customer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_create_new_hall_as_customer(self):
        res = self.client().post("/halls", json=self.new_hall, headers = customer_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_update_hall_as_customer(self):
        res = self.client().patch("/halls/2", json=self.update_hall, headers = customer_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')
    
    def test_delete_hall_as_customer(self):
        res = self.client().delete('/halls/1', headers = customer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['code'], 'forbidden')
        self.assertEqual(data['description'], 'Permission not found.')


if __name__ == "__main__":
    unittest.main()
    