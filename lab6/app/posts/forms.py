from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateTimeLocalField
from datetime import datetime
from app.posts.models import Tag, User

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
    author_id = SelectField("Author", coerce=int)
    tags = SelectMultipleField("Tags", coerce=int)  # нове поле


    submit = SubmitField("Add Post")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.posts.models import User
        # Завантажуємо користувачів із БД для вибору автора
        self.author_id.choices = [(u.id, u.username) for u in User.query.order_by(User.id).all()]
        self.tags.choices = [(t.id, t.name) for t in Tag.query.order_by(Tag.id).all()]
