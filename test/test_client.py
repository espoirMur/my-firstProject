import unittest
from app import create_app,db
from app.models import Employee,Role
from flask import url_for
import re

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app('testing')
        self.app_context=self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client=self.app.test_client(use_cookies=True)
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    def test_home_page(self):
        response= self.client.get(url_for('home.homepage'))
        self.assertTrue('Utapata' in response.get_data(as_text=True))
    def test_login_register(self):
        # trying the registration of a new account
        response=self.client.post(url_for('auth.register'), data={
            'email':'test@test.com',
            'username':'test',
            'password':'test',
            'password2':'test'

        })
        self.assertTrue(response.status_code==302)

       #trying the login with a new account
        response=self.client.post(url_for('auth.login'),data={
            'email':'test@test.com',
            'password':'test'
        },follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertTrue(re.search('Hi,\s+test'),data)
        self.assertTrue('you have not confirmed your account yet in ',data)

       #sending authetification token
        emp=Employee.query.filter_by(email='test@test.com').first()
        token=emp.generate_confirmation_token()
        response=self.client.get(url_for('confirm',token=token),follow_redirect=True)
        data=response.get_data(as_text=True)
        self.assertTrue('You have confirmed your account' in data)

        #logout user

        response = self.client.get(url_for('auth.logout'),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have been logged out' in data)

