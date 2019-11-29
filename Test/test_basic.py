import sys
import unittest
from url_shortener import create_app, db, short 
from flask import Flask
from requests_toolbelt import MultipartEncoder
class FlaskTestCase(unittest.TestCase):

    #Checking whether the server is working
    def test_server_run(self):
        response = create_app()
        page = response.test_client().get("/")
        self.assertEqual(page.status_code, 200)
        self.assertIn(b'SHORT URL GENERATOR', page.data)
    #Checking redirection to login page while trying to access logs without a session
    def test_logs_redirect(self):
        response = create_app()
        page = response.test_client().get("/logs")
        self.assertEqual(page.status_code, 302)

        #Checking if accessing add_link with a null request results in a 404
    def test_add_link_404(self):
        response = create_app()
        page = response.test_client().get("/add_link")
        self.assertEqual(page.status_code, 404)
        self.assertIn(b'404 PAGE NOT FOUND', page.data)


        #Checking login page access
    def test_login(self):
        response = create_app()
        page = response.test_client().get("/login")
        self.assertEqual(page.status_code, 200)

         #Checking login page bypass with wrong credentials
    def test_login_wrong_credentials(self):
        response = create_app()
        data = MultipartEncoder(
            fields={
                "Username": "admin",
                "Password": "password"
            }
        )
        headers = {"Content-Type": data.content_type}
        page = response.test_client().post("/login",data=data, headers=headers)
        self.assertEqual(page.status_code, 200)
        self.assertIn(b'Login Failed',page.data)

        #Checking login page bypass with correct credentials
    def test_login_correct_credentials(self):
        response = create_app()
        data = MultipartEncoder(
            fields={
                "Username": "admin",
                "Password": "password1050"
            }
        )
        headers = {"Content-Type": data.content_type}
        page = response.test_client().post("/login",data=data, headers=headers)
        self.assertEqual(page.status_code, 302)

    def test_add_link_with_invalid_url(self):
        response = create_app()
        data = MultipartEncoder({"Original_URL": "http://www.google.com"})
        headers = {"Content-Type": data.content_type}
        page = response.test_client().post("/add_link",data=data, headers=headers)
        self.assertEqual(page.status_code, 200)
        self.assertIn(b'Short URL generated successfully!', page.data)

    def test_logs_redirection(self):
        response = create_app()
        data = MultipartEncoder(
            fields={
                "Username": "admin",
                "Password": "password1050"
            }
        )
        headers = {"Content-Type": data.content_type}
        page = response.test_client().post("/login",data=data, headers=headers,follow_redirects=True)
        self.assertEqual(page.status_code, 200)
        self.assertIn(b'Login Successful!', page.data)