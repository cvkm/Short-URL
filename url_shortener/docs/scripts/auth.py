import string
from datetime import datetime
from random import choices
from sqlalchemy.orm import validates
from extensions import db
import logging 

""" Creating the Database for the **Admin Panel** """
class Admin(db.Model):
    """ Creating the *admin* table """
    username = db.Column(db.String(5), primary_key=True)
    password = db.Column(db.String(256))
    Attempts = db.Column(db.Integer, default = 0)
    User_Address = db.Column(db.String(128))
