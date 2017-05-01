from flask import render_template
from . import main
from flask_login import login_required

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'


