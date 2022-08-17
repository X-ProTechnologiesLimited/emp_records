from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from .models import User

class RegisterForm(FlaskForm):
    email = StringField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    name = StringField(
        'name',
        validators=[DataRequired()])
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    dob = DateField(
        'dob',
        validators=[DataRequired()]
    )

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class PasswordReset(FlaskForm):
    email = StringField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    dob = StringField(
        'dob',
        validators=[DataRequired()]
    )

    def validate(self):
        initial_validation = super(PasswordReset, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append("This email is not registered")
            return False
        if self.dob.data != user.dob:
            self.dob.errors.append("The date of birth does not match our records!")
            return False
        return True


class PasswordChange(FlaskForm):
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    def validate(self):
        initial_validation = super(PasswordChange, self).validate()
        if not initial_validation:
            return False
        return True

class SelfPasswordChange(FlaskForm):
    curr_password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    def validate(self):
        initial_validation = super(SelfPasswordChange, self).validate()
        if not initial_validation:
            return False
        return True
