from flask import Flask
from .extensions import db
from .routes import short
import logging
import os
def create_app(config_file='settings.py'):

    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    app.register_blueprint(short)
    logging.basicConfig(filename='server.log',level=logging.DEBUG)
    
    app.secret_key = os.urandom(24)

    return app