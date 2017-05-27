from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
class EditProfileForm(Form):
	name = StringField('Real name', validators=[Length(0,64)])
	location = StringField('Location', validators=[Length(0,64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit Your Edit')

