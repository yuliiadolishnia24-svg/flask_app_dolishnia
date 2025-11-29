from flask import Blueprint, render_template

products_bp = Blueprint('products', __name__, template_folder='templates')

@products_bp.route("/list")
def product_list():
    products = ["Яблуко", "Банан", "Апельсин"]
    return render_template("products/list.html", products=products)
