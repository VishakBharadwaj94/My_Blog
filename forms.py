from wtforms import Form,StringField,PasswordField,TextAreaField,RadioField,validators
from wtforms.fields.html5 import EmailField

class RegistrationForm(Form):

	
	name = StringField('Name',[validators.Length(min=4,max=25)])
	username = StringField('Username',[validators.Length(min=4,max=25)])
	email =EmailField('Email address', [validators.DataRequired(), validators.Email()])
	password = PasswordField('Password',[
		validators.Length(min=4,max=25),
		validators.DataRequired(),
		validators.EqualTo('confirm',message="Passwords don't match!")
		])
	confirm = PasswordField('Confirm Password')