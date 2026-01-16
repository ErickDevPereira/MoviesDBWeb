from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from data_handling import get_data_by_title

class LoginForm(FlaskForm):
    username: StringField = StringField("Username:", validators = [DataRequired(message = 'Empty username is invalid')])
    password: PasswordField = PasswordField("Password", validators = [
                                                    DataRequired(message = 'Empty password is invalid'),
                                                    Length(min = 8, max = 128, message = 'Length of password must be between 8 and 128 characteres')
                                                    ])
    submit: SubmitField = SubmitField('Login')

class RegisterForm(FlaskForm):
    username: StringField = StringField("Username", validators = [
                                                    DataRequired(message = 'Empty username is invalid'),
                                                    Length(min = 4, max = 64, message = 'The number of characters for username must be between 4 and 64 characteres')
                                                    ])
    password: PasswordField = PasswordField("Password", validators = [
                                                    DataRequired(message = 'Empty password is invalid'),
                                                    Length(min = 8, max = 128, message = 'Length of password must be between 8 and 128 characteres')
                                                    ])
    conf_password: PasswordField = PasswordField("Confirm your password", validators = [
                                                                        DataRequired(message = 'Empty password is invalid'),
                                                                        EqualTo('password', message = 'The passowrds must match') 
                                                                        ])
    email: StringField = StringField("Email", validators = [
                                            Email(message = 'Invalid format for email'),
                                            DataRequired(message = 'Empty email is invalid')
                                            ])
    phone: StringField = StringField("Phone", validators = [
                                            Length(min = 4, max = 30, message = 'The length for phone must be between 4 and 30 characteres'),
                                            DataRequired(message = 'Empty phone is invalid')
                                            ])
    submit: SubmitField = SubmitField("Create Account")

class SearchMovieForm(FlaskForm):
    title: StringField = StringField("Write the title of a movie that you know:", validators = [DataRequired(message = 'Empty title is not allowed!')])
    submit: SubmitField = SubmitField("")

    def validate_title(self, field: StringField) -> None:
        """
        Explanation:
        This method will check if the title searched by the user is present on the API. If it is not found, a ValidationError
        will be raised, charging its string inside form.title.errors.

        Parameters:
        field: will represent the title attibute.
        """
        if get_data_by_title(field.data) is None:
            raise ValidationError(f'The movie {field.data} couldn\'t be found. Try again!')

class CommentForm(FlaskForm):
    comment: TextAreaField = TextAreaField("Write your comment about this movie:", validators = [DataRequired(message = "The comment must have some text")])
    submit: SubmitField = SubmitField("SEND")