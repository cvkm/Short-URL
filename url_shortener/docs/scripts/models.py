import string
from datetime import datetime
from random import choices
from sqlalchemy.orm import validates
from extensions import db
import logging 
from flask import flash, redirect, url_for


class Link(db.Model):
    """ Creates the table *Link* in the database """
    id = db.Column(db.Integer, primary_key=True)
    Original_URL = db.Column(db.String(1024))
    Short_URL = db.Column(db.String(6), unique=True)
    Clicks = db.Column(db.Integer, default=0)
    Date_Created = db.Column(db.DateTime, default=datetime.now)
    User_Address = db.Column(db.String(128))

    def __init__(self, **kwargs):
        """ Calls upon the **generate_short_link** method for generating the *Short URL* """
        super().__init__(**kwargs)
        self.Short_URL = self.generate_short_link()

    def generate_short_link(self):
        """ Uses random choices to generate a *Short URL* path of length **six** characters """
        characters = string.digits + string.ascii_letters
        Short_URL = ''.join(choices(characters, k=6))
        link = self.query.filter_by(Short_URL=Short_URL).first()

        if link:
            return self.generate_short_link()
        
        return Short_URL
