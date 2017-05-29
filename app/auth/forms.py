from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,EqualTo
from ..models import User
from wtforms import ValidationError

class LoginForm(FlaskForm):
    User_name=StringField('User name',validators=[Required(),Length(1,64)])
    password=PasswordField('Password',validators=[Required()])
    remember_me=BooleanField('Keep me logged in')
    submit=SubmitField('Log In')

class RegisterForm(FlaskForm):
    user_name=StringField('User name',validators=[Required(),Length(1,64)])
    password=PasswordField('Password',validators=[Required(),EqualTo('password2',message='Password must match.')])
    password2=PasswordField('Confirm password',validators=[Required()])
    protect_answer=StringField('Please input the answer',validators=[Required(),Length(1,64)])    
    submit=SubmitField('submit')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
              raise ValidationError('Username already in use')
