from flask import Flask, render_template

# Імпорт блюпринтів
from app.users.views import users_bp
from app.products.views import products_bp

def create_app():
    app = Flask(__name__)

    # Реєстрація блюпринтів
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(products_bp, url_prefix="/products")

    # Головний маршрут, щоб не було 404 на '/'
    @app.route("/")
    def index():
        return render_template("base.html", content="""
            <h1>Ласкаво просимо до Flask додатку!</h1>
            <p>Перейдіть у <a href='/users/hi/John'>Users</a> або <a href='/products/list'>Products</a></p>
        """)

    return app
