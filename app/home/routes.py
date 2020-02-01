# -*- coding: utf-8 -*-
from app import app
from . import home
from flask import render_template, session, redirect, url_for, request
from flask_login import login_required
from app import db
from textblob import TextBlob as blob
from sqlalchemy.sql import func

from app.home.forms import Comment_Form
from ..models import  Reviews, Movies



def get_avg_rating(movie_id):
    avg_rating = db.session.query(func.avg(Reviews.rating).label('average')).filter(Reviews.movie_id==movie_id).scalar()
    if(avg_rating):
        avg_rating += 0.01
        avg_rating = round(avg_rating, 0)
        return avg_rating
    else:
        return 'No rating yet'

def get_review_num(movie_id):
    nor = Reviews.query.filter_by(movie_id=movie_id).count() #number of reviews
    return nor

@home.route('/movie/<movie_id>')
@login_required 
def movie(movie_id):
    form = Comment_Form()
    movie_id = movie_id
    movie = Movies.query.filter_by(id=movie_id).first_or_404()
    comments = Reviews.query.filter_by(movie_id=movie_id).order_by(Reviews.timestamp.desc())
    nor = Reviews.query.filter_by(movie_id=movie_id).count() #number of reviews
    if(not comments):
        comments = None
    return render_template('home/single_movie.html', movie=movie, title='Welcome', form=form, comments=comments, nor=nor)

@home.route('/comment/<movie_id>', methods=['GET','POST'])
@login_required 
def comment(movie_id):
     form = Comment_Form()
     if form.validate_on_submit():
        user_id = session['user_id']
        comment_obj = blob(form.comment.data)
        rating = comment_obj.sentiment.polarity
        rating = round(rating, 1)
        if rating <= -0.7:
            rating = 1
        elif rating > -0.7 and rating <= -0.2:
            rating = 2
        elif rating > -0.2 and rating <=0.1:
            rating = 3
        elif rating > 0.1 and rating <= 0.6:
            rating = 4
        else:
            rating = 5
        review = Reviews(comment=form.comment.data,
                         rating = rating,
                         user_id = user_id,
                         movie_id = movie_id
                     )
        db.session.add(review)
        db.session.commit()
        avg_rating = get_avg_rating(movie_id)
        movie = Movies.query.filter_by(id=movie_id).first_or_404()
        movie.avg_rating =  avg_rating
        db.session.commit()
        return redirect(url_for('home.movie', movie_id=movie_id))

@home.route('/')
@home.route('/index')
@login_required 
def home():
    page = request.args.get('page', 1, type=int)
    movies = Movies.query.order_by(Movies.avg_rating.desc()).paginate(page, 3, False)
    return render_template('home/index.html', movies=movies, nor=get_review_num, title='Welcome')

        
