from wtforms import Form, StringField, PasswordField, SubmitField, validators


class LoginForm(Form):
    username = StringField('Username', [
        validators.DataRequired(message='Username is required.'),
        validators.Length(min=4, max=20, message='Username must be between 4 and 20 characters.')
    ])
    password = PasswordField('Password', [
        validators.DataRequired(message='Password is required.'),
        validators.Length(min=6, max=20, message='Password must be at least 6 characters long.'),
    ])
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    username = StringField('Username', [
        validators.DataRequired(message='Username is required.'),
        validators.Length(min=4, max=20, message='Username must be between 4 and 20 characters.')
    ])
    email = StringField('Email Address', [
        validators.DataRequired(message='Email is required.'),
        validators.Length(min=6, max=35, message='Email must be between 6 and 35 characters.'),
        validators.Email(message='Invalid email address.')
    ])
    password = PasswordField('New Password', [
        validators.DataRequired(message='Password is required.'),
        validators.Length(min=6, max=20, message='Password must be at least 6 characters long.'),
    ])
