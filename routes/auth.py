"""Route pour l'authentification des utilisateurs."""

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from models.user import User
from utils.decorators import login_required
from utils.helpers import is_strong_password

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    """Authentification des utilisateurs."""
    user_controller = current_app.user_controller

    if session.get("user") and request.method == "GET":
        flash("Vous êtes déjà connecté.", "info")
        return redirect(url_for("main.home"))

    errors = {}
    form = {}

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        form["username"] = username

        if not username:
            errors["username"] = "Le nom d'utilisateur est requis."
        if not password:
            errors["password"] = "Le mot de passe est requis."

        user = None
        if not errors:
            user = user_controller.get_by_username(username)
            if user is None or not user.verify_password(password):
                errors["password"] = "Nom d'utilisateur ou mot de passe incorrect."

        if errors:
            return render_template("auth/login.html", errors=errors, form=form)

        user_controller.db.execute(
            "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
            user.id,
        )

        session["user"] = user.to_session()
        flash("Connexion réussie, bienvenue sur ESIGELEATS !", "success")

        next_url = request.args.get("next")
        return redirect(next_url or url_for("main.home"))

    return render_template("auth/login.html", errors=errors, form=form)


@bp.route("/logout", endpoint="logout")
@login_required
def logout(current_user):
    """Déconnexion des utilisateurs."""
    session.pop("user", None)
    flash(f"Vous avez été déconnecté ({current_user['username']})", "info")
    return redirect(url_for("auth.login"))


@bp.route("/register", methods=["GET", "POST"], endpoint="register")
def register():
    """Inscription des nouveaux utilisateurs."""
    user_controller = current_app.user_controller

    if session.get("user") and request.method == "GET":
        flash("Vous êtes déjà connecté.", "info")
        return redirect(url_for("main.home"))

    errors = {}
    form = {}

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        display_name = request.form.get("display_name", "").strip()
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")

        form["username"] = username
        form["display_name"] = display_name

        if not username:
            errors["username"] = "Le nom d'utilisateur est requis."
        elif user_controller.get_by_username(username) is not None:
            errors["username"] = "Ce nom d'utilisateur est déjà utilisé."

        if not display_name:
            errors["display_name"] = "Le nom de profil est requis."

        if not password:
            errors["password"] = "Le mot de passe est requis."
        elif not is_strong_password(password):
            errors["password"] = (
                "Le mot de passe doit contenir au moins 8 caractères, "
                "une majuscule, une minuscule, un chiffre et un caractère spécial."
            )

        if not password_confirm:
            errors["password_confirm"] = "Merci de confirmer votre mot de passe."
        elif password != password_confirm:
            errors["password_confirm"] = "Les mots de passe ne correspondent pas."

        if errors:
            return render_template("auth/register.html", errors=errors, form=form)

        user = User(username=username, password_hash="")
        user.display_name = display_name
        user.hash_and_set_password(password)
        user_controller.create_user(user)

        session["user"] = user.to_session()
        flash("Inscription réussie, bienvenue sur ESIGELEATS !", "success")
        return redirect(url_for("main.home"))

    return render_template("auth/register.html", errors=errors, form=form)
