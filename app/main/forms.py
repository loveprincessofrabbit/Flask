from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_pagedown.fields import PageDownField

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    body=PageDownField("Please input",validators=[Required()])
    submit=SubmitField('Submit')

