"""Route principale du site web"""

from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.route("/", endpoint="home")
def home():
    """Page d'accueil du site web."""
    return render_template("home.html")


@bp.route("/not-implemented", methods=["GET"], endpoint="not_implemented")
def not_implemented():
    """Page indiquant qu'une fonctionnalité n'est pas encore implémentée."""
    return render_template("errors/not_implemented.html")
