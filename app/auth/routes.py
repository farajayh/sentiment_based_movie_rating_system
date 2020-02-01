# -*- coding: utf-8 -*-
from app import app

from flask import flash, render_template, url_for, redirect, session
from flask_login import login_required, login_user, logout_user, current_user 
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth
from app import db, login_manager
from app.auth.forms import Login_Form, Registration_Form, Change_Password_Form
from ..models import Users

@auth.route('/register', methods=['GET','POST'])
def register():
    form = Registration_Form()
    if form.validate_on_submit():
        user = Users(email=form.email.data,
                     username=form.username.data,
                     password_hash=generate_password_hash(form.password.data, method='sha256')
                     )
        db.session.add(user)
        db.session.commit()
        flash('You have registered successfully')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/single_movie/<movie_name>', methods=['GET', 'POST'])
def single_movie(movie_name):
    pass

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_Form()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('home.home'))
        else:
            flash('Invalid login details')
            
    return render_template('auth/login.html', form=form, title='Login')
    
@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = Change_Password_Form()
    if form.validate_on_submit():
        if check_password_hash(current_user.password_hash, form.old_password.data):
            current_user.password_hash = generate_password_hash(form.new_password.data, method='sha256')
            db.session.commit()
            flash('Your password has been changed')
            return render_template('auth/change_password.html', form=form, title='Change Password')
        else:
            flash('Invalid password')
            return render_template('auth/change_password.html', form=form, title='Change Password')
            
    return render_template('auth/change_password.html', form=form, title='Change Password')
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('auth.login'))
        
'''@app.route('/login', methods=['GET', 'POST'])
def login():
    output = [x for x in request.form.values()]
    return render_template('login.html', out=output)'''