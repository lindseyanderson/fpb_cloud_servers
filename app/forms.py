from flask.ext.wtf import Form
from wtforms import TextField,PasswordField
from wtforms.validators import Required

class LoginForm(Form):
	username = TextField('rs_username', validators = [Required()])
	apikey   = PasswordField('rs_apikey', validators = [Required()])
