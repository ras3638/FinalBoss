from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    UserName = TextField('UserName', validators = [Required()])
    Password = TextField('Password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)