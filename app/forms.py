from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

from app.models import User


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("That email is already registered.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class TweetForm(FlaskForm):
    body = TextAreaField(
        "What's happening?", validators=[DataRequired(), Length(max=280)]
    )
    submit = SubmitField("Tweet")


class EditProfileForm(FlaskForm):
    bio = TextAreaField("Bio", validators=[Length(max=160)])
    submit = SubmitField("Save Changes")
