# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 21:29:31 2019

@author: Olaitan
"""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
#initialize the flask app
app = Flask(__name__)

import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__)) #base directory (neccessary for setting the database)

class Config(object):
    SECRET_KEY = 'this-is-the-key' #secret keys for forms and sessions
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') #set the database uri
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True   #enable automatic commit of database changes at the end of each request
    SQLALCHEMY_TRACK_MODIFICATIONS = False #disable signaling the app anytime a database change is made
    UPLOAD_FOLDER = os.path.join(basedir, 'static/movie_cover')
    
app.config.from_object(Config)
#Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_message = 'Input Your Email and password'
login_manager.login_view = 'auth.login'
migrate = Migrate(app, db)

from app import models

#registering blueprint
from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

from .home import home as home_blueprint
app.register_blueprint(home_blueprint)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

