from flask.ext.wtf import Form
from wtforms import BooleanField, PasswordField, TextField
from wtforms.validators import Required

class LoginForm(Form):
    #This class is used to login
    UserName = TextField('UserName', validators = [Required()])
    Password = PasswordField('Password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)


class SignupForm(Form):

    #This class is used to to sign up

    SignupUserName = TextField('SignupUserName', validators = [Required()])
    SignupPassword = PasswordField('SignupPassword', validators = [Required()])

    remember_me = BooleanField('remember_me', default = False)

class CreateEntryForm(Form):

    #This class is used to create an entry in ToDo List

    title = TextField('title', validators = [Required()])
    entry = TextField('entry', validators = [Required()])



