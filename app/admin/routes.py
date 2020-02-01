# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from app import app
from . import admin
import os

from flask import flash, render_template, url_for, redirect, session, request
from flask_login import login_required, login_user, logout_user, current_user 
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.sql import func

from app import db
from app.admin.forms import Login_Form, Change_Password_Form
from ..models import Users, Movies, Reviews


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

@admin.route('/')
@admin.route('/index')
def home():
    if not 'admin_logged_in' in session:
        return redirect(url_for('admin.login'))
    page = request.args.get('page', 1, type=int)
    movies = Movies.query.order_by(Movies.avg_rating.desc()).paginate(page, 3, False)
    return render_template('admin/index.html', movies=movies, nor=get_review_num, title='Welcome')

@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_Form()
    if form.validate_on_submit():
        user = Users.query.filter_by(username='Admin').first()
        if user is not None and check_password_hash(user.password_hash, form.password.data):
            session['admin_user_id'] = user.id
            session['admin_username'] = user.username
            session['admin_logged_in'] = True
            return redirect(url_for('admin.home'))
        else:
            flash('Invalid login details')
            
            
    return render_template('admin/login.html', form=form, title='Login')

accept = set(['jpg', 'jpeg', 'gif', 'png'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in accept

@admin.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if not 'admin_logged_in' in session:
        return redirect(url_for('admin.login'))
    
    if request.method == 'POST':
        if 'movie_cover' not in request.files:
            flash('No file part')
            return redirect(request.url)
        movie_cover = request.files['movie_cover']
        if movie_cover.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if movie_cover and allowed_file(movie_cover.filename):
            filename = secure_filename(movie_cover.filename)
            movie_cover.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            movie_name = request.form['movie_name']
            movie_desc = request.form['movie_desc']
            genre = request.form['genre']
            movie_cover = secure_filename(movie_cover.filename)
            movie = Movies(movie_name=movie_name,
                     movie_desc=movie_desc,
                     movie_genre=genre,
                     movie_photo=movie_cover
                     )
            db.session.add(movie)
            db.session.commit()
            flash('You have added a new movie successfully')
    return render_template('admin/add_movie.html', title='Add Movie')

@admin.route('/movie/<movie_id>')
@login_required 
def movie(movie_id):
    if not 'admin_logged_in' in session:
        return redirect(url_for('admin.login'))
    
    movie_id = movie_id
    movie = Movies.query.filter_by(id=movie_id).first_or_404()
    comments = Reviews.query.filter_by(movie_id=movie_id)
    nor = Reviews.query.filter_by(movie_id=movie_id).count() #number of reviews
    if(not comments):
        comments = None
    return render_template('admin/single_movie.html', movie=movie, title='Welcome', comments=comments, nor=nor)
    
@admin.route('/delete/<movie_id>')
@login_required 
def delete(movie_id):
    if not 'admin_logged_in' in session:
        return redirect(url_for('admin.login'))
    
    movie_id = movie_id
    movie = Movies.query.filter_by(id=movie_id).first_or_404()
    db.session.delete(movie)
    reviews = Reviews.query.filter_by(id=movie_id)
    for review in reviews:
        db.session.delete(review)
    db.session.commit()
    return redirect(url_for('admin.home'))

@admin.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if not 'admin_logged_in' in session:
        return render_template('admin/login.html', title='Welcome')
    form = Change_Password_Form()
    if form.validate_on_submit():
        if check_password_hash(current_user.password_hash, form.old_password.data):
            current_user.password_hash = generate_password_hash(form.new_password.data, method='sha256')
            db.session.commit()
            flash('Your password has been changed')
            return render_template('admin/change_password.html', form=form, title='Change Password')
        else:
            flash('Invalid password')
            return render_template('admin/change_password.html', form=form, title='Change Password')
            
    return render_template('admin/change_password.html', form=form, title='Change Password')
    
@admin.route('/logout')
def logout():
    if not 'admin_logged_in' in session:
        return render_template('admin/login.html', title='Welcome')
    del session['admin_logged_in']
    flash('You have been logged out')
    return redirect(url_for('admin.login'))
   