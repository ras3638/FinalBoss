from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    #This class is used to login
    UserName = TextField('UserName', validators = [Required()])
    Password = TextField('Password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class SignupForm(Form):

    #This class is used to to sign up

    SignupUserName = TextField('SignupUserName', validators = [Required()])
    SignupPassword = TextField('SignupPassword', validators = [Required()])

    remember_me = BooleanField('remember_me', default = False)