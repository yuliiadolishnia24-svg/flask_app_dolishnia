from flask import Blueprint, render_template, request, redirect, session, url_for, flash, abort
from app.extensions import db
from app.posts.models import Post, User
from app.posts.forms import PostForm

posts_bp = Blueprint("posts", __name__, url_prefix="/post", template_folder='templates')

# --- Створення поста ---
@posts_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            user_id=form.author_id.data,  # прив'язка до користувача
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            category=form.category.data
            
        )


        # --- додавання тегів ---
        from app.posts.models import Tag
        selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        post.tags.extend(selected_tags)

        db.session.add(post)
        db.session.commit()
        flash(f"Post '{post.title}' has been added.", "success")
        return redirect(url_for("posts.all_posts"))
    return render_template("posts/add_post.html", form=form)

# --- Відображення всіх постів ---
@posts_bp.route("/", methods=["GET"])
def all_posts():
    posts = Post.query.filter_by(is_active=True).order_by(Post.posted.desc()).all()
    return render_template("posts/posts.html", posts=posts)

# --- Перегляд конкретного поста ---
@posts_bp.route("/<int:id>", methods=["GET"])
def detail_post(id):
    post = Post.query.get_or_404(id)
    return render_template("posts/detail_post.html", post=post)

# --- Редагування поста ---
@posts_bp.route("/<int:id>/update", methods=["GET", "POST"])
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)
    form.publish_date.data = post.posted
    if form.validate_on_submit():
        form.populate_obj(post)
        post.posted = form.publish_date.data
        post.user_id = form.author_id.data
        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for("posts.detail_post", id=post.id))
    return render_template("posts/add_post.html", form=form, title="Edit Post")

# --- Видалення поста ---
@posts_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    post = Post.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully.", "danger")
        return redirect(url_for("posts.all_posts"))
    return render_template("posts/delete_confirm.html", post=post)
