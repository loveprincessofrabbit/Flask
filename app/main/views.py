from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app
from flask_login import login_required, current_user
from . import main
from .forms import PostForm
from .. import db
from ..models import Permission, Role, User, Post
from ..decorators import admin_required

@main.route('/',methods=['GET','POST'])
def index():
    form=PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post=Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page=request.args.get('page',1,type=int)
    pagination=Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=20,error_out=False)
    posts=pagination.items
    return render_template('index.html',form=form,posts=posts,pagination=pagination)

@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

