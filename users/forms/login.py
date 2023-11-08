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
