"""Gestion des erreurs HTTP personnalisées pour l'application Flask."""

from flask import Blueprint, render_template

bp = Blueprint("errors", __name__)


@bp.app_errorhandler(404)
def not_found_error(e):
    """Page d'erreur 404 : Not Found."""
    return render_template("errors/404.html"), 404


@bp.app_errorhandler(500)
def internal_error(e):
    """Page d'erreur 500 : Internal Server Error."""
    return render_template("errors/500.html"), 500


@bp.app_errorhandler(405)
def method_not_allowed_error(e):
    """Page d'erreur 405 : Method Not Allowed."""
    return render_template("errors/405.html"), 405


@bp.app_errorhandler(403)
def forbidden_error(e):
    """Page d'erreur 403 : Forbidden."""
    return render_template("errors/403.html"), 403


@bp.app_errorhandler(401)
def unauthorized_error(e):
    """Page d'erreur 401 : Unauthorized."""
    return render_template("errors/401.html"), 401


@bp.app_errorhandler(422)
def unprocessable_entity_error(e):
    """Page d'erreur 422 : Unprocessable Entity."""
    return render_template("errors/422.html"), 422


@bp.app_errorhandler(503)
def service_unavailable_error(e):
    """Page d'erreur 503 : Service Unavailable."""
    return render_template("errors/503.html"), 503
