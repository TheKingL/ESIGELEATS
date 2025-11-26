"""Définitions des décorateurs pour les routes Flask."""

from functools import wraps

from flask import flash, jsonify, redirect, session, url_for


def login_required(f):
    """Décorateur pour exiger une connexion utilisateur."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get("user")
        if not user:
            flash("Merci de vous connecter pour accéder à cette page.", "error")
            return redirect(url_for("auth.login"))
        return f(user, *args, **kwargs)

    return decorated_function


def admin_required(f):
    """Décorateur pour exiger des permissions admin."""

    @wraps(f)
    def decorated_function(current_user, *args, **kwargs):
        if not current_user or not current_user.get("is_admin"):
            flash(
                "Vous n'avez pas les permissions nécessaires pour accéder à cette page.",
                "error",
            )
            return redirect(url_for("main.home"))

        return f(current_user, *args, **kwargs)

    return decorated_function


def api_login_required(f):
    """Décorateur pour les routes API qui nécessitent une connexion utilisateur."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get("user")
        if not user:
            return jsonify({"error": "auth_required"}), 401
        return f(user, *args, **kwargs)

    return decorated_function


def api_admin_required(f):
    """Décorateur pour les routes API qui nécessitent des permissions admin."""

    @wraps(f)
    def decorated_function(current_user, *args, **kwargs):
        if not current_user.get("is_admin"):
            return jsonify({"error": "forbidden"}), 403
        return f(current_user, *args, **kwargs)

    return decorated_function
