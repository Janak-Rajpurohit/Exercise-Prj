from flask_wtf import FlaskForm
# from wtforms.form import Form
from flask_wtf.file import FileAllowed,FileField
from wtforms import StringField,PasswordField,SubmitField, BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
import email_validator
from excercise.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
                        #label , validating that it's not empty data is required
    username=StringField('Username',validators=[DataRequired(),Length(min=5,max=20)])  #username between 5 to 20
    email = StringField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])  #equal to password field

    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("The username is taken. Please chose a different username.")
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("The email already exists.")
        
class UpdateAccountForm(FlaskForm):
                        #label , validating that it's not empty data is required
    username=StringField('Username',validators=[DataRequired(),Length(min=5,max=20)])  #username between 5 to 20
    email = StringField("Email", validators=[DataRequired(),Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])

    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("The username is taken. Please chose a different username.")
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("The email already exists.")

class LoginForm(FlaskForm):
                        #label , validating that it's not empty data is required
    email = StringField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    # keeps user login for sometime by cookies
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
