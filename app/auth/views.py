import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm,RegisterForm

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.User_name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user=User(username=form.user_name.data,password=form.password.data,protect_answer=form.protect_answer.data)
        db.session.add(user)
        flash('success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        
