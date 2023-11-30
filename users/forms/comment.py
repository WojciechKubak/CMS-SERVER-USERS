from wtforms import Form, StringField, IntegerField, validators


class CommentForm(Form):
    """
    CommentForm Class

    This class defines a WTForms-based form for validating comment input.

    Attributes:
        content (StringField): A StringField for the comment content with data validation.
        article_id (IntegerField): An IntegerField for the article ID with data validation.
        user_id (IntegerField): An IntegerField for the user ID with data validation.
    """
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
