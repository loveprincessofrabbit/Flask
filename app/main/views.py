import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from flask import Flask,request,render_template, redirect, url_for, abort, flash, request,\
    current_app,make_response
from flask_login import login_required, current_user
import os
from . import main
from .forms import PostForm,EditProfileForm,CommentForm,Reset
from .. import db
from ..models import Permission, Role, User, Post,Comment
from ..decorators import admin_required,permission_required
reload(sys)


@main.route('/',methods=['GET','POST'])
def index():
    form=PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post=Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page=request.args.get('page',1,type=int)
    show_followed=False
    if current_user.is_authenticated:
        show_followed=bool(request.cookies.get('show_followed',''))
    if show_followed:
        query=current_user.followed_posts
    else:
        query=Post.query
    pagination=query.order_by(Post.timestamp.desc()).paginate(page,per_page=20,error_out=False)
    posts=pagination.items
    return render_template('index.html',form=form,posts=posts,show_followed=show_followed,pagination=pagination)

@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            21
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=20,
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)

@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    post=Post.query.get_or_404(id)
    form=PostForm()
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    if form.validate_on_submit():
        post.body=form.body.data
        db.session.add(post)
        flash('upgrade succeed')
        return redirect(url_for('.post',id=post.id))
    form.body.data=post.body   
    return render_template("edit.html",form=form)

@main.route('/user/<username>')
def user(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html',user=user)

@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form=EditProfileForm()
    if form.validate_on_submit():
        current_user.name=form.name.data
        current_user.location=form.name.data
        current_user.about_me=form.about_me.data
        avatar=request.files['avatar']
        fname=avatar.filename
        UPLOAD_FOLDER='/root/python/aaaaa/app/static/user_head/'
        ALLOWED_EXTENSIONS=['png','jpg','jpeg','gif']
        flag='.' in fname and fname.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
        if not flag:
            flash('ERROR EXTENSIONS')
            return redirect(url_for('.user',username=current_user.username))
        avatar.save('{}{}_{}'.format(UPLOAD_FOLDER,current_user.username,fname))
        current_user.real_avatar='/static/user_head/{}_{}'.format(current_user.username,fname)
        db.session.add(current_user)
        flash('Your profile has been updated')
        return redirect(url_for('.user',username=current_user.username))
    form.name.data=current_user.name
    form.location.data=current_user.location
    form.about_me=current_user.about_me
    return render_template('edit_profile.html',form=form)

@main.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user=User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.username=form.username.data
        user.role=Role.query.get(form.role.data)
        user.name=form.name.data
        user.location=form.location.data
        user.about_me=form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user',username=user.username))
    form.username.data=user.username
    form.role.data=user.role_id
    form.name.data=user.name
    form.location.data=user.location
    form.about_me.data=user.about_me
    return render_template('edit_profile.html',form=form,user=user)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user',username=username))
    current_user.follow(user)
    flash('You are now following %s.'% username)
    return redirect(url_for('.user',username=username))

@main.route('/followers/<username>')
def followers(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page=request.args.get('page',1,type=int)
    pagination=user.followers.paginate(page,per_page=20,error_out=False)
    follows=[{'user':item.follower,'timestamp':item.timestamp} for item in pagination.items]
    return render_template('followers.html',user=user,title="Followers of",endpoint='.followers',pagination=pagination,follows=follows)

@main.route('/all')
@login_required
def show_all():
    resp=make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','',max_age=30*24*60*60)
    return resp

@main.route('/followed')
@login_required
def show_followed():
    resp=make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','1',max_age=30*24*60*60)
    return resp

@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))

@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=20,error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)

@main.route('/find_passowrd',methods=['GET','POST'])
def find_password():
    form=Reset()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:
            flash('No this user')
            return redirect(url_for('.find_password'))
        else:
            if form.answer.data==user.protect_answer:
                user.password=form.password.data
                flash('succeed')
            else:
                flash('answer Error')
                return redirect(url_for('.find_password'))
    return render_template('Reset_password.html',form=form)
