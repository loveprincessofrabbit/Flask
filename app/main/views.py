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
#alter here
@main.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first()
	if user is  None:
		abort(404)
	return render_template('user.html',user=user)
#alter here
@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validator_on_submit():
		current_user.name = form.name.data
		current_user.location = form.location.data
		current_user.about_me = form.about_me.data
		db.session.add(current_user)
		flash('Your profile has been updated')
		return redirect(url_for('.user',username=current_user.username))
	form.name.data = current_user.name
	form.location.data = current_user.loaction
	form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', form=form)



