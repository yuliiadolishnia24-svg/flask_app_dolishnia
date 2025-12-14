from datetime import datetime
from sqlalchemy import Enum
from app.extensions import db

# --- Модель користувача ---
class User(db.Model):
    __tablename__ = "users"  # 🔹 обов’язково, щоб ForeignKey працював
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    # Зв'язок один-до-багатьох: один користувач → багато постів
    posts = db.relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"


# --- Асоціативна таблиця для Many-to-Many Post ↔ Tag ---
post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True)
)



# --- Модель поста ---
class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # ForeignKey на User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", name="fk_posts_user_id"), nullable=True)

    user = db.relationship("User", back_populates="posts")

    posted = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(
        Enum("news", "publication", "tech", "other", name="category_enum"),
        default="other"
    )
    is_active = db.Column(db.Boolean, default=True)

    # Many-to-Many: теги
    tags = db.relationship(
        "Tag",
        secondary=post_tags,
        back_populates="posts"
    )

    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"


# --- Модель тегів ---
class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Many-to-Many: пости
    posts = db.relationship(
        "Post",
        secondary=post_tags,
        back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag {self.name}>"
