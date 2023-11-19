from wtforms import Form, StringField, IntegerField, validators


class CommentForm(Form):
    content = StringField('Content', validators=[
        validators.DataRequired(),
        validators.Length(max=2000, message='Content must be no more than 2000 characters')
    ])

    article_id = IntegerField('Article ID', validators=[
        validators.DataRequired(),
        validators.NumberRange(min=1, message='Article ID must be a positive integer')
    ])

    user_id = IntegerField('User ID', validators=[
        validators.DataRequired(),
        validators.NumberRange(min=1, message='User ID must be a positive integer')
    ])
