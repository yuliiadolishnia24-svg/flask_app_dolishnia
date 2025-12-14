from datetime import datetime
from sqlalchemy import Enum
from app.extensions import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), default="Anonymous")
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(
        Enum("news", "publication", "tech", "other", name="category_enum"),
        default="other"
    )

    # Нові поля
    is_active = db.Column(db.Boolean, default=True)
    author = db.Column(db.String(20), default="Anonymous")

    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"
