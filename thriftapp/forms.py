from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField,PasswordField,DateField,SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf.file import FileField,FileAllowed,FileRequired


class SignupForm(FlaskForm):
    firstname = StringField("Firstname",validators=[DataRequired(message="hello, name required")])
    lastname = StringField("Lastname",validators=[DataRequired(message="hello, name required")])
    dateofbirth=DateField("DateOfBirth", validators=[DataRequired()])
    email = StringField("Your Email",validators=[Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password",validators=[EqualTo("password",message="Must match password")])
    phone=StringField("Phone-number",validators=[DataRequired()])
    Homeadd=StringField("Home-Address",validators=[DataRequired()])
    empadd=StringField("Employment-Address",validators=[DataRequired()])
    btn = SubmitField("Sign Up!")


class Verform(FlaskForm):
    firstname = StringField("Firstname",validators=[DataRequired(message="hello, name required")])
    lastname = StringField("Lastname",validators=[DataRequired(message="hello, name required")])
    dateofbirth=DateField("DateOfBirth", validators=[DataRequired()])
    email = StringField("Your Email",validators=[Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password",validators=[EqualTo("password",message="Must match password")])
    phone=StringField("Phone-number",validators=[DataRequired()])
    Homeadd=StringField("Home-Address",validators=[DataRequired()])
    empadd=StringField("Employment-Address",validators=[DataRequired()])
    btn = SubmitField("Click to get verified")


class ProfileForm(FlaskForm):
    fullname = StringField("Fullname",validators=[DataRequired(message="hello, full name required")])
    pix= FileField("Display Picture",validators=[FileRequired(),FileAllowed(['jpg','png'],'Images only!')])
    btn = SubmitField("Update Profile!")
  
class ContactForm(FlaskForm):
    fullname=StringField("Fullname",validators=[DataRequired(message="name is required")])
    confirm_name=StringField("confirm_fullname",validators=[DataRequired(message="Haba"),EqualTo("fullname",message="Do you mean this name is same as above?")])
    email=StringField("email",validators=[Email()])
    message=TextAreaField("message")
    btn=SubmitField("Send Message")

class ContactUs(FlaskForm):
    fullname=StringField("fullname",validators=[DataRequired()])
    phone=StringField("Phone",validators=[DataRequired()])
    email=StringField("Email",validators=[Email()])
    message=TextAreaField("Message")
    btn=SubmitField("Send Message")
 
    
    
    
     
    

