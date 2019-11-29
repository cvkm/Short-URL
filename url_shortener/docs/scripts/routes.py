""" 
All the **routes** are defined 
"""

from flask import Blueprint, render_template, request, redirect, flash, url_for, session,g
import os
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from extensions import db
from models import Link
from auth import Admin
from urllib.parse import urlparse, urljoin
import time

short = Blueprint('short', __name__)
@short.route('/<Short_URL>')
def redirect_to_url(Short_URL):
    """ 
    Redirects to *Original URL* upon accessing *Short URL* and increases the visits of the *Short URL* by **one** in the database

    :type Short_URL: string
    :param Short_URL: **Six** random characters
    """
    link = Link.query.filter_by(Short_URL=Short_URL).first_or_404()
    link.Clicks = link.Clicks + 1
    db.session.commit()
    return redirect(link.Original_URL)


@short.before_request
def before_request():
    """ 
    Checks for **user** in session
    """
    g.user = None
    if 'user' in session:
        g.user = session['user']

@short.route('/')
def index():
    """ 
    Loads the **Home page** and stores the logs of visitor
    """
    logging.debug("Service accessed")
    ip =  request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    links = Link.query.order_by(Link.id.desc()).filter_by(User_Address  = ip)
    return render_template('home.html', links = links)


@short.route('/add_link', methods=['POST'])
def add_link():
    """ 
    Retrieves the *Original URL* from user, validates whether the URL is valid or not, converts it into *Short URL* and stores both in the database.
    Loads the **add link page** displaying both the *Original URL* and the *Short URL*
    """
    Original_URL = request.form['Original_URL']
    parsed = urlparse(urljoin(Original_URL, '/'))
    # parsed = urlparse(Original_URL)
    check1 = Original_URL.find('www',0,len(Original_URL))
    if check1 == -1:
        checkP = 'N'
    else :
        checkP = 'Y'
    if bool(all([parsed.scheme, parsed.path, parsed.netloc])) != False and ((checkP =='N' and len(parsed.netloc.split(".")) > 1) or (checkP =='Y' and len(parsed.netloc.split(".")) > 2)):
            ip =  request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            link = Link(Original_URL=Original_URL, User_Address = ip)
            db.session.add(link)
            db.session.commit()
            logging.debug("Link generated successfully!")
            flash("Short URL generated successfully!")
            links = Link.query.order_by(Link.id.desc()).filter_by(User_Address  = ip)
            return render_template('link_added.html', 
                new_link=link.Short_URL, Original_URL=link.Original_URL, links = links)
    else:
        flash("The URL entered is invalid. Please include 'http://' or any other valid scheme.")   
        return redirect(url_for('short.index'))

@short.route('/logs')
# @requires_auth
def stats():
    """ 
    **Checks** whether the *user* in session has **access** to the logs.
    If user has access, then it loads the **logs page** dispalying the stats related to Links *else* the user is redirected to the **login page**
    """
    if g.user:
        links = Link.query.order_by(Link.id.desc()).all()
        ip =  request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        logging.warning("Database is being accessed by " + ip)
        return render_template('logs.html', links=links)

    return redirect(url_for('short.auth'))


@short.route('/login', methods = ['POST', 'GET'])
def auth():
    """ 
    Loads the **login page** and validates the responses of the user.
    Upon successful validation the user is redirected to the **logs page**
    """
    session.pop('user',None)
    admin = Admin.query.filter_by(username="admin").first()
    ip =  request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if request.method == 'POST':
        session.pop('user',None)
        username = request.form['Username']
        password = request.form['Password']
        User = Admin.query.first()
        hashed = check_password_hash(User.password, password)
        if username == User.username and hashed == True:
            admin = Admin.query.filter_by(username="admin").first()
            admin.Attempts = 0
            admin.User_Address = ip
            db.session.commit()
            session['user'] = username
            flash("Login Successful!")
            return redirect(url_for('short.stats'))
        else: 
            admin = Admin.query.filter_by(username="admin").first()
            admin.Attempts = admin.Attempts + 1
            db.session.commit()
            flash("Login Failed.")
            
    return render_template('auth.html')


@short.errorhandler(404)
def page_not_found(e):
    """ 
    Throws a *404* error, for page not found.
    """
    logging.error("Bad Request")
    return render_template('bad.html'), 404