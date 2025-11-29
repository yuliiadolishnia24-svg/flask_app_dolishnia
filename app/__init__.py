from flask import Flask, render_template

# Імпорт блюпринтів
from app.users.views import users_bp
from app.products.views import products_bp
from app.accounts import accounts_bp  # <- новий blueprint

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"  # Для сесій та flash

    # Реєстрація блюпринтів
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(accounts_bp, url_prefix="/accounts")  # <- новий blueprint

    # Головний маршрут, щоб не було 404 на '/'
    @app.route("/")
    def index():
        return render_template("base.html", content="""
            <h1>Ласкаво просимо до Flask додатку!</h1>
            <p>Перейдіть у <a href='/users/hi/John'>Users</a> або <a href='/products/list'>Products</a> або <a href='/accounts/login'>Login</a></p>
        """)

    return app
