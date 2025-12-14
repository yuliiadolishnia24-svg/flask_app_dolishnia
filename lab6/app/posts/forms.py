from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from datetime import datetime
from wtforms.fields import DateTimeLocalField

CATEGORIES = [
    ("news", "News"),
    ("publication", "Publication"),
    ("tech", "Tech"),
    ("other", "Other"),
]

class PostForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(min=2, max=150)]
    )
    content = TextAreaField(
        "Content",
        validators=[DataRequired()]
    )
    is_active = BooleanField("Active Post", default=True)
    publish_date = DateTimeLocalField(
        "Publish Date",
        format="%Y-%m-%dT%H:%M",
        default=datetime.now
    )
    category = SelectField(
        "Category",
        choices=CATEGORIES,
        validators=[DataRequired()]
    )
    submit = SubmitField("Add Post")
