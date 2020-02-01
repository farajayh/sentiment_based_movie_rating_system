# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 17:19:53 2019

@author: Olaitan
"""

from app import db
from app import login_manager
from flask_login import UserMixin
from datetime import datetime

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(70), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    review = db.relationship('Reviews', backref='posted_by', lazy='dynamic')
        
    def __repr__(self):
        return '{}'.format(self.username)
    
    
class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key= True)
    comment = db.Column(db.Text, index=True)
    rating = db.Column(db.Float, index=True)
    timestamp = db.Column(db.String, index=True, default=datetime.strftime(datetime.utcnow(), '%b %d %Y, %H:%M:%S'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    
    def __repr__(self):
        return '<Comment {}>'.format(self.comment)

    
class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key= True)
    movie_name = db.Column(db.String(100), index=True)
    movie_desc = db.Column(db.Text, index=True)
    movie_genre = db.Column(db.Text, index=True)
    movie_photo = db.Column(db.String(100), index=True)
    avg_rating = db.Column(db.Float, index=True, default=None)
    review = db.relationship('Reviews', backref='comment_on', lazy='dynamic')
    
    def __repr__(self):
        return '<Movie {}>'.format(self.movie_name)
    

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))