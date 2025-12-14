from datetime import datetime
from sqlalchemy import Enum
from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    posts = db.relationship("Post", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(
        Enum("news", "publication", "tech", "other", name="category_enum"),
        default="other"
    )
    is_active = db.Column(db.Boolean, default=True)

    # ForeignKey з ім'ям обмеження
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", name="fk_posts_user_id"), nullable=True)
    user = db.relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"
