import os
from flask import Flask
from app.extensions import db, migrate


def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True, template_folder="posts/templates" )

    # 🔹 TESTING режим (для unittest)
    if config_name == "testing":
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SECRET_KEY"] = "test"
        app.config["WTF_CSRF_ENABLED"] = False

    # 🔹 NORMAL режим
    else:
        app.config.from_object("app.config.Config")

        db_path = os.path.join(app.instance_path, "data.sqlite")
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # 🔹 імпорт моделей (щоб Alembic їх бачив)
    from app.posts.models import Post

    # 🔹 реєстрація blueprint (ВАЖЛИВО для маршрутів)
    from app.posts.routes import posts_bp
    app.register_blueprint(posts_bp)

    # 🔹 Тестовий маршрут
    @app.route("/hello")
    def hello():
        return "Hello World!"

    return app
