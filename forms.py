from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.fields import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
#from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class


# the login form
class LoginForm(FlaskForm):
    username = TextField('Username', validators=[DataRequired(), Length(min=5)])
    password = PasswordField('Passwort', validators=[DataRequired()])
    active = BooleanField('Active', default=True)

    
