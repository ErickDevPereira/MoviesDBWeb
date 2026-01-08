from wtforms import StringField, SubmitField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Email, Length

class LoginForm(FlaskForm):
    username = StringField("Username:", validators = [DataRequired(message = 'Empty username is invalid')])
    password = PasswordField("Password", validators = [
                                                    DataRequired(message = 'Empty password is invalid'),
                                                    Length(min = 8, max = 128, message = 'Length of password must be between 8 and 128 characteres')
                                                    ])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField("Username", validators = [
                                                    DataRequired(message = 'Empty username is invalid'),
                                                    Length(min = 4, max = 64, message = 'The number of characters for username must be between 4 and 64 characteres')
                                                    ])
    password = PasswordField("Password", validators = [
                                                    DataRequired(message = 'Empty password is invalid'),
                                                    Length(min = 8, max = 128, message = 'Length of password must be between 8 and 128 characteres')
                                                    ])
    conf_password = PasswordField("Confirm your password", validators = [
                                                                        DataRequired(message = 'Empty password is invalid'),
                                                                        EqualTo('password', message = 'The passowrds must match') 
                                                                        ])
    email = StringField("Email", validators = [
                                            Email(message = 'Invalid format for email'),
                                            DataRequired(message = 'Empty email is invalid')
                                            ])
    phone = StringField("Phone", validators = [
                                            Length(min = 4, max = 30, message = 'The length for phone must be between 4 and 30 characteres'),
                                            DataRequired(message = 'Empty phone is invalid')
                                            ])
    submit = SubmitField("Create Account")